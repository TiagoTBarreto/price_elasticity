# Elasticidade de Preço - Bestbuy.com

<p align="center">
  <img src="https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/84157c15-e41e-436b-8751-031061869d54" width="100%" height="500">
</p>

# 1. Problema de Negócio
A BestBuy.com, uma das principais varejistas online de eletrônicos, oferece uma vasta gama de produtos, incluindo televisores, laptops, acessórios e serviços digitais. Em um mercado altamente competitivo com consumidores sensíveis a preços, a empresa busca otimizar suas estratégias de precificação para maximizar receita e lucratividade.

A loja enfrenta dificuldades na determinação de preços ideais devido a uma base de clientes diversificada e concorrentes frequentes em promoções e descontos. Sem entender a reação dos diferentes segmentos de consumidores às mudanças de preço, a empresa pode perder vendas, definir preços subótimos e comprometer a margem de lucro.

**Objetivo do Projeto:**
Através de um projeto de elasticidade de preço prever como alterações nos preços afetarão a demanda por diferentes produtos. O objetivo é fornecer insights baseados em dados para informar decisões de precificação e otimizar promoções.


# 2. Ferramentas Utilizadas

**Ferramentas para Análise de Dados**
- Python 3.11.4: A linguagem de programação principal usada para desenvolver o projeto.
- Estatística para Análise dos Dados.

**Biblioteca para cálculo da Elasticidade :**
- Statsmodels: Biblioteca para modelagem estatística que fornece classes e funções para a estimativa de muitos modelos estatísticos diferentes, incluindo modelos de regressão OLS (Ordinary Least Squares) para calcular elasticidades.
  
**Desenvolvimento e Controle de Versão:**
- Git: Ferramenta de versionamento de código para rastrear alterações.
- Pyenv (Ambiente Virtual): Utilizado para isolar dependências e gerenciar versões do Python.

**Exposição dos Resultados:**
- Streamlit WebApp: Criado para disponibilizar o acesso aos resultos a qualquer usuário e também simulações de faturamento com base nos descontos.

**Habilidades e Abordagem:**
- Pensamento Crítico e Resolução de Problemas: Habilidades fundamentais aplicadas para analisar, solucionar problemas e tomar decisões ao longo do projeto.
  

# 3. Descrição dos Dados 
    
| Coluna         | Descrição                                                                                     |
|----------------|-----------------------------------------------------------------------------------------------|
| `Date_imp`     | Data e hora da transação                                                          |
| `Category_name`| Categoria do produto, incluindo características como tipo e função (e.g., "speaker, portable, bluetooth"). |
| `name`         | Nome do produto.                                                                     |
| `price`        | Preço do produto                                                       |
| `merchant`     | Nome da loja                                   |
| `brand`        | Marca do produto.                                                                             |
| `currency`     | Moeda utilizada, normalmente USD (dólar americano).                              |
| `weight`       | Peso do produto, incluindo a unidade de medida (e.g., "14 pounds").                           |


# 4. Exploração dos Dados 
## 4.1 Mês
- Mês 4 registrou poucas transações
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/33bdb6bf-2554-44f9-b731-a09472c54de0)

## 4.2 Merchant
- Merchant com maior volume foi o Bestbuy.com
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/ab3c6d58-8296-4714-9d60-51990106a842)

## 4.3 Marca
- Apple e Sony são as marcas com maior volume de transações.
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/6356f3f8-8260-498c-bd63-3d79d7541e72)

### 4.3.1 Apple
- Dois produtos com registro de venda outlier com valores perto de 0.
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/50d96cea-c5c8-496e-b8e9-fb8f7eb7fbb6)

### 4.3.2 Sony
- Um produto com registro de venda outlier com valores perto de 0.
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/99792831-ad89-4254-a2ae-d5dc5575d2c7)


# 5. Premissas assumidas para a análise
  - Foram consideradas as transações do mês 05-2017 até 12-2017, pois devido ao baixo número de transações no mês 4 geraria muitos valores faltantes posteriomente.
  - O merchant selecionado foi "Bestbuy.com" devido a ser o mais representativo na base.
  - Filtrar preço acima de $5.00 para remover os outliers encontrados na Apple e Sony, marcas com maior demanda na Bestbuy.com
  - Não foram considerados produtos que tinham mais de 2 meses sem transações.
    
# 6. Elasticidade-Preço da Demanda:
- Medida que indica a sensibilidade na demanda de um produto em relação a variações no preço. Pode ser calculada com a seguinte fórmula, onde Q = Quantidade (Demanda) e P = Preço
  
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/9def2fa9-7cf0-48aa-ab18-3cf4fe3d1950)

## 6.1 Elasticidade Positiva x Negativa:
- Positiva: e = 5 -> Um aumento de 1% no preço leva a um aumento de 5% na demanda.
- Negativa: e = -5 -> Um aumento de 1% no preço leva a uma redução de 5% na demanda.
  
## 6.2 Tipos de Elasticidade:
**Para definir esses tipos vamos considerar a elasticidade como negativa. Ou seja aumento no preço diminuição na demanda.**
- Elastíca: quando o valor da elasticidade é maior que 1 -> Muito sensível a alterações de preço.
- Inelastíca: quando o valor da elasticidade é menor que 1 -> Grande potencial de lucro.
- Unitária: valor da elasticidade é igual a 1 -> Moderadamente sensíveis.

# 7. Machine Learning
- Como mencionado anteriormente, uma das variáveis essenciais para calcular a elasticidade é a relação entre as diferenças de Quantidade e Preço. Para investigar essa relação, apliquei o método dos Mínimos Quadrados Ordinários (OLS) para encontrar o coeficiente de regressão entre preço e quantidade de cada produto individualmente, que indica a magnitude e direção dessa relação.
- Para garantir a robustez dos resultados, considerei apenas os coeficientes que alcançaram uma significância estatística de 95%.
- Dos 485 produtos analisados, somente 43 mostraram uma relação entre preço e quantidade que foi estatisticamente significativa.

## 7.1 Visualização da Elasticidade
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/42932ef4-5850-4a35-9e4d-46f568febdc5)

# 8.0 Business Performance
## 8.1 Simulação:
- Dos 43 produtos selecionados anteriormente realizei uma filtragem pelos que tiveram vendas em Dezembro de 2017 para a simulação, resultando em 24 produtos.
- O desconto para os produtos de elasticidade negativa foi de 25%.
- O aumento para os produtos de elasticidade positiva foi de 10%.
- Só foram considerados dos 24 produtos, aqueles que tiveram um aumento no faturamento em relação a Dezembro de 2017 de 30%.
## 8.2 Resultado:
- Faturamento Dezembro 2017 sem otimização de preços: $56437.73
- Expectativa faturamento Janeiro 2018 com otimização de preços: $174840.04
- Crescimento no Faturamento: 209.79%


# 9.0 Elasticidade Cruzada entre Produtos
**Objetivo: Identificar relação entre os produtos.**

## 9.1 Diferença entre produto Complementar e Substituto:
1. **Complementar:** São os produtos que tem Elasticidade Negativa: Então uma diminuição no preço do produto A aumenta a demanda pelo produto B.
- Exemplo: Elasticidade = 2 -> Uma diminuição de 2% no preço do produto A aumenta a demanda em 4% do produto B.
2. **Substituto:** São os produtos que tem Elasticidade Positiva: Então um aumento no preço do produto A aumenta a demanda pelo produto B.
- Exemplo: Elasticidade = 5 -> Um aumento de 2% no preço do Produto A aumenta a demanda em 10% do produto B.

## 9.2 Produtos Complementares
- **Diminuindo o preço do produto em destaque aumenta a demanda pelos produtos complementares.**
- **Realizar Cross-Sell, oferecendo os produtos listados junto do desconto.**
### 9.2.1 Produto 1: YU2 Powered Desktop Speakers (Matte Black)
1. Kanto - sub6 6 80W Powered Subwoofer - Gloss Black"
2. SRS-ZR7 Wireless Speaker
3. sub6 100W 6 Active Subwoofer (Matte Gray)
4. SRS-XB40 Bluetooth Speaker (Black)
5. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR

### 9.2.2 Produto 2: Sony MDR-1A Headphone - Black (International Version U.S. warranty may not apply)
1. SanDisk - Ultra 500GB Internal SATA Solid State Drive for Laptops
2. Sandisk Extreme CompactFlash Memory Card - 64 GB (SDCFXS-064G-A46)
3. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"
4. Panasonic - Lumix G85 Mirrorless Camera with 12-60mm Lens - Black
5. SanDisk Extreme 500 480GB USB 3.0 Portable SSD (Solid State Drive) - SDSSDEXT-480G

### 9.2.3 Produto 3: Kanto - sub6 6 80W Powered Subwoofer - Gloss Black"
1. SRS-ZR7 Wireless Speaker
2. sub6 100W 6 Active Subwoofer (Matte Gray)
3. YU2 Powered Desktop Speakers (Matte Black)
4. SRS-XB40 Bluetooth Speaker (Black)
5. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"

## 9.3 Produtos Substitutos
- Aumentando o preço do produto em destaque aumenta a demanda pelos produtos substitutos.
- Se necessário desovar estoque, oferecer os produtos listados junto do aumento do produto em destaque.

### 9.3.1 Produto 1: SanDisk Extreme 500 480GB USB 3.0 Portable SSD (Solid State Drive) - SDSSDEXT-480G
1. Sandisk Extreme CompactFlash Memory Card - 64 GB (SDCFXS-064G-A46)
2. SanDisk - Ultra 500GB Internal SATA Solid State Drive for Laptops

### 9.3.2 Produto 2: WD - Blue 500GB Internal SATA Hard Drive
1. SanDisk Ultra II 1TB SATA III SSD - 2.5-Inch 7mm Height Solid State Drive - SDSSDHII-1T00-G25

# 10. O produto final do projeto
WebApp online, hospedado no Streamlit Cloud, está disponível para acesso em qualquer dispositivo conectado à internet, possibilitando que qualquer consumidor tenha acesso aos resultados e possa realizar simulações de faturamento com diferentes descontos e aumentos. Você pode acessar o WebApp através do seguinte link: https://price-elasticity-bestbuy.streamlit.app/

## 10.1 Home
- Na aba Gráfico tem uma explicação sobre elasticidade positiva e negativa e um gráfico.
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/e3ac19c9-8251-43ff-b50d-88917cb68915)

- Na aba Dataframe é possível baixar um arquivo csv com todas as métricas do OLS (p-valor, R2)
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/f9571c4b-66d0-44fc-88e3-7d2ec25d496d)


## 10.2 Business Performance
- Na aba Resultado é possível calcular o faturamento previsto e o aumento percentual com base no desconto e aumento escolhido e também filtrar os produtos pelo aumento no faturamento.
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/263b94ae-c7bd-4eab-8500-8e09673ff9f4)

- Na aba Dataframe é possível baixar um arquivo csv com os valores antigos e após a previsão:
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/95f3b6d6-5e9c-45c3-8d86-a3c3ccb7f44b)

## 10.3 Cross Elasticity
- Na aba Insights tem explicações sobre o que é um Produto Complementar e Substituto e recomendações de cross-sell e também de desova de estoque.
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/2f648d4c-a404-4ec7-a7f8-81c6f728a58b)

- Na aba Dataframe é possível baixar um arquivo csv com os produtos e sua elasticidade e também realizar filtros de produto complementar e subsituto.
![image](https://github.com/TiagoTBarreto/streamlit-taxi/assets/137197787/13f7d788-0d1a-4b81-b528-64d973be3311)



