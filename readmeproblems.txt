Contar a história das ideias iniciais e como elas mudaram...


Example:
Problem: this happended...
Solution: this was done...


Problem: 20 websites detectados para webscraping e a ideia era criar
um pipeline com maior informações de preços possível. Obviamente, 
após 3 webscrapings, percebeu-se que seria uma tarefa muito demorada.
Solution: usar o que ja se tinha e, visto que
o carrefour.com possuia o maior número de aparelhos com preços
possiveis de se obter e foi optado seguir com ele.

Problem: webscraping de 4mil links é muito perigoso, se o código cai voce perde tudo.
Solution: fazer um método de salvar num backup dentro do loop. Parece óbvio, mas para
quem esta no começo essa ideia pode demorar um pouco para surgir. Salvar é muito menos
demorado (0.1s) do que fazer um request.get() num website (~2segundos).

Problem: Dados técnicos não seriam rapidamente obtidos pelos webscrapings
dos sites de e-commerce, e tomaria-se muito tempo, além de dificil,
de separar os dados técnicos de cada aparelho através de um código.
Outra coisa: haveriam poucos dados técnicos.

Solution: Procurou-se outras fontes, e encontrou-se o tudocelular.com.
Parece óbvio, mas não foi pensado isso no início, já que mts websites de
venda de celulares possuem uma ficha de produto mais completa.

Problem: O site do tudocelular.com é completíssimo, mostrando quase 100 
variáveis técnicas para cada celular. Porém, poucos aparelhos tem o valor registrado.
A solução é linkar os dados coletados com esse site com os dados encontrados pelos
sites de e-commerce. O problema é que esta sendo muito dificil de implementar essa
conexão.

Solução: o site do jacotei.com fornece os preços dos celulares, mas com muito menos
dados de informações técnicas dos celulares (o que diminuiria a "elasticidade"
do modelo de machine learning). Porém, para concluir o deadline, é visto como uma solução
mais rápida...


NO FIM, escrever o que aprendi com isso...

conclusão: se voce pode usar um trabalho já feito por outros, sem necessariamente ter que
gerar os dados você mesmo, faça...

