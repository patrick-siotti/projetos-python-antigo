# teste de acertividade

Esse é um script em python básico usado para testar a acertividade de apostas automatizadas na binance futuros, usando estratégias basicas de compra e vende em relação a variações salvas em um banco de dados. Em si ele tem conceitos bem básicos mas ainda foi um sucesso mesmo estando em protótipo.

- arquivo principal de teste: main_estr_apren.py

# funcionamento do script

 - parte 1:

   O script primeiramente passa dez das primeiras variações do ativo até a variação mais recente em tempos variados tentando encontrar padrões, nesse caso, se caso um padrão ocorrer mais de 5 vezes (pode ser modificado no script) com mais de 80% de acertividade (pode ser modificado no script), tendo mais que 1% de variação sobre o valor do ativo (pode ser modificado no script), aquele padrão é colocado como um padrão ativo no tempo determinado da quele ativo.

   As partes que podem ser modificadas no script são em relação a abertura da estratégia, se a estratégia vai ser mais livre ou mais privada em relação aos dados dos padrões, podendo deixar os padrões mais ou menos acertivos.

 - parte 2:

   Depois de pegar os padrões daquele ativo, ele começa a percorrer o ativo de forma ao vivo, vendo cada mudança dele em tempos variados, verificando os padrões que estão e que não estão como ativos, para ver se não encontrou um novo padrão ou se um padrão que ocorria no passado não esta mais funcionando.

 - parte 3:

   Quando um padrão for detectado na linha do tempo, o script simula uma aposta, verificando se a aposta seria ou não bem sucessida.

O projeto foi descontinuado.
