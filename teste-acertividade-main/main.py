from binance.client import Client
from apibinance import api_key, api_secret
import numpy as np
import pandas as pd
import time
import win32api

#login client
client = Client(api_key, api_secret)

#sincronizing a server time
gt = client.get_server_time()
tt=time.gmtime(int((gt["serverTime"])/1000))
win32api.SetSystemTime(tt[0],tt[1],0,tt[2],tt[3],tt[4],tt[5],0)

def last_close(synbol, interval):
    return client.futures_historical_klines(synbol, interval, '1d')[-2][4]

def all_candles(synbol, interval, limit='4w'):
    return client.futures_historical_klines(synbol, interval, limit)

def all_closes(candles):
    return [close[4] for close in candles]

def give_rsi(close):
    close = pd.Series(close)
    close = pd.Series(close).astype(float)
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return list(rsi)

def pega_media_movel(close):
    close = pd.Series(close)
    close = pd.Series(close).astype(float)
    ma_25 = close.rolling(window=25).mean()
    ma_50 = close.rolling(window=50).mean()
    ma_100 = close.rolling(window=100).mean()
    return list(ma_25), list(ma_50), list(ma_100)

def entende_media(ma_25, ma_50, ma_100, n=-2):
    tipo = None

    if type(n) == int:

        ma_25 = ma_25[n]
        ma_50 = ma_50[n]
        ma_100 = ma_100[n]

        if ma_25 > ma_50 > ma_100:
            tipo = 'subindo'
        elif ma_25 < ma_50 < ma_100:
            tipo = 'descendo'
        elif ma_25 < ma_50 > ma_100 and ma_25 > ma_100 < ma_50:
            tipo = 'tendencia_descendo'
        elif ma_25 < ma_100 > ma_50 and ma_25 > ma_50 < ma_100:
            tipo = 'tendencia_subindo'
    return tipo

# for tempo in ['1m', '15m', '30m', '1h', '4h']:
#     print(f'\n\ntempo de {tempo}')
velas = all_candles('btcusdt', '1m')
fechamentos = all_closes(velas)
# arquivo = open('fechamentos.txt', 'r')
# fechamentos = eval(arquivo.read())
# arquivo.close()

rsi = give_rsi(fechamentos)
ma_25, ma_50, ma_100 = pega_media_movel(fechamentos)

arquivo = open('fechamentos.txt', 'w')
arquivo.write(str(fechamentos))
arquivo.close()

# print(fechamentos[-2])
# print(f'{rsi[-2]:.2f}')
# print(ma_25[-2])
# print(ma_50[-2])
# print(ma_100[-2])
# print(entende_media(ma_25, ma_50, ma_100))

# criar uma estratégia em que se caso o rsi estiver a baixo de 30, e as médias móveis estiverem indicando subida, é pra apostar que vai subir, e o mesmo ao contrario quando o rsi estiver a cima de 70, ou 40 60 tb
print('\nestrategia 1')
max_rsi = 70
min_rsi = 30
media_max = ['descendo',] # 'tendencia descendo'
media_min = ['subindo',] # 'tendencia subindo'
curva = None
mudanca = []
acertos = 0
erros = 0

for n, close in enumerate(fechamentos):
    close = float(close)
    if curva != None:
        if curva == 'descendo':
            if close < mudanca[0]:
                acertos += 1
                curva = None
                mudanca = []
            elif close > mudanca[1]:
                erros += 1
                curva = None
                mudanca = []
        elif curva == 'subindo':
            if close > mudanca[0]:
                acertos += 1
                curva = None
                mudanca = []
            elif close < mudanca[1]:
                erros += 1
                curva = None
                mudanca = []        

    if curva == None:
        # if rsi[n] > max_rsi or rsi[n] < min_rsi:
        #     print(rsi[n], entende_media(ma_25, ma_50, ma_100))
        if rsi[n] > max_rsi and entende_media(ma_25, ma_50, ma_100, n) in media_max:
            mudanca.append(close - (close / 100))
            mudanca.append(close + (close / 100))
            curva = 'descendo'

        elif rsi[n] < min_rsi and entende_media(ma_25, ma_50, ma_100, n) in media_min:
            mudanca.append(close + (close / 100))
            mudanca.append(close - (close / 100))
            curva = 'subindo'

if acertos == 0 and erros == 0:
    acert = 0
else:
    acert = (100*acertos)/(acertos+erros)

print(f'acertos: {acertos}\nerros: {erros}\nacertividade: {acert:.2f}%')

    # # criar a mesma de cima, mas só pode ser uma de cima e depois uma de baixo respectivamentes

    # print('\nestrategia 2')
    # max_rsi = 60
    # min_rsi = 40
    # media_max = ['descendo',] # 'tendencia descendo'
    # media_min = ['subindo',] # 'tendencia subindo'
    # curva = None
    # mudanca = []
    # acertos = 0
    # erros = 0
    # antes = None

    # for n, close in enumerate(fechamentos):
    #     close = float(close)
    #     if curva != None:
    #         if curva == 'descendo':
    #             if close < mudanca[0]:
    #                 acertos += 1
    #                 curva = None
    #                 mudanca = []
    #             elif close > mudanca[1]:
    #                 erros += 1
    #                 curva = None
    #                 mudanca = []
    #         elif curva == 'subindo':
    #             if close > mudanca[0]:
    #                 acertos += 1
    #                 curva = None
    #                 mudanca = []
    #             elif close < mudanca[1]:
    #                 erros += 1
    #                 curva = None
    #                 mudanca = []        

    #     if curva == None:
    #         # if rsi[n] > max_rsi or rsi[n] < min_rsi:
    #         #     print(rsi[n], entende_media(ma_25, ma_50, ma_100))
    #         if rsi[n] > max_rsi and entende_media(ma_25, ma_50, ma_100, n) in media_max and (antes==None or antes=='min'):
    #             mudanca.append(close + (close / 100))
    #             mudanca.append(close - (close / 100))
    #             curva = 'subindo'
    #             antes = 'min'

    #         elif rsi[n] < min_rsi and entende_media(ma_25, ma_50, ma_100, n) in media_min and (antes==None or antes=='max'):
    #             mudanca.append(close - (close / 100))
    #             mudanca.append(close + (close / 100))
    #             curva = 'descendo'
    #             antes = 'max'

    # if acertos == 0 and erros == 0:
    #     acert = 0
    # else:
    #     acert = (100*acertos)/(acertos+erros)

    # print(f'acertos: {acertos}\nerros: {erros}\nacertividade: {acert:.2f}%')

    # # criar a mesma da primeira, mas se caso a média movel n seguir, ele vai guardar que chegou pra quando indicar subida, apostar

    # print('\nestrategia 3')
    # max_rsi = 20
    # min_rsi = 80
    # media_max = ['descendo',] # 'tendencia descendo'
    # media_min = ['subindo',] # 'tendencia subindo'
    # curva = None
    # mudanca = []
    # acertos = 0
    # erros = 0
    # esperando = False

    # for n, close in enumerate(fechamentos):
    #     close = float(close)
    #     if curva != None:

    #         if esperando == True:
    #             if curva == 'subindo':
    #                 if entende_media(ma_25, ma_50, ma_100, n) in media_min and rsi[n-1] > rsi[n]:
    #                     esperando = False
    #             if curva == 'descendo':
    #                 if entende_media(ma_25, ma_50, ma_100, n) in media_max and rsi[n-1] < rsi[n]:
    #                     esperando = False

    #         if esperando == False:
    #             if curva == 'descendo':
    #                 if close < mudanca[0]:
    #                     acertos += 1
    #                     curva = None
    #                     mudanca = []
    #                 elif close > mudanca[1]:
    #                     erros += 1
    #                     curva = None
    #                     mudanca = []
    #             elif curva == 'subindo':
    #                 if close > mudanca[0]:
    #                     acertos += 1
    #                     curva = None
    #                     mudanca = []
    #                 elif close < mudanca[1]:
    #                     erros += 1
    #                     curva = None
    #                     mudanca = []        

    #     if curva == None:
    #         # if rsi[n] > max_rsi or rsi[n] < min_rsi:
    #         #     print(rsi[n], entende_media(ma_25, ma_50, ma_100))
    #         if rsi[n] > max_rsi and entende_media(ma_25, ma_50, ma_100, n) in media_max and rsi[n-1] > rsi[n]:
    #             mudanca.append(close - (close / 100))
    #             mudanca.append(close + (close / 100))
    #             curva = 'descendo'

    #         elif rsi[n] < min_rsi and entende_media(ma_25, ma_50, ma_100, n) in media_min and rsi[n-1] < rsi[n]:
    #             mudanca.append(close + (close / 100))
    #             mudanca.append(close - (close / 100))
    #             curva = 'subindo'

    #         elif rsi[n] > max_rsi and entende_media(ma_25, ma_50, ma_100, n) not in media_max and rsi[n-1] > rsi[n]:
    #             mudanca.append(close - (close / 100))
    #             mudanca.append(close + (close / 100))
    #             curva = 'descendo'
    #             esperando = True

    #         elif rsi[n] < min_rsi and entende_media(ma_25, ma_50, ma_100, n) not in media_min and rsi[n-1] < rsi[n]:
    #             mudanca.append(close + (close / 100))
    #             mudanca.append(close - (close / 100))
    #             curva = 'subindo'
    #             esperando = True

    # if acertos == 0 and erros == 0:
    #     acert = 0
    # else:
    #     acert = (100*acertos)/(acertos+erros)

    # print(f'acertos: {acertos}\nerros: {erros}\nacertividade: {acert:.2f}%')