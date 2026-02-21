# Página explicando a metodologia

# Importações
import dash_bootstrap_components as dbc
from dash import html, dcc

# Layout da página
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Metodologia", className="display-4 text-primary fw-bold mb-4"),
            dcc.Markdown('''
                
### Fonte dos Dados
A base de todo o trabalho são os registros oficiais do **Portal de Dados Abertos da Câmara dos Deputados**. Para quem deseja auditar a metodologia ou entender os detalhes mais técnicos de extração e processamento, o código-fonte está disponível em nosso [repositório público](https://github.com/ricardo-grandi-bianco/bussola-da-camara).

### Seleção das Votações
Para garantir que a Bússola mostre a posição real de cada parlamentar, aplicamos filtros rigorosos. Primeiro, consideramos apenas as votações nominais realizadas no Plenário da Câmara para garantir uma comparação justa entre todos os deputados (excluímos as votações nas comissões, pois nem todos participam delas). 

Em seguida, descartamos votações unânimes ou simbólicas, pois, se há consenso, o voto não serve para identificar quem é de esquerda, liberal, conservador ou progressista. 

Por fim, aplicamos um critério de frequência mínima: apenas deputados que deram votos válidos em pelo menos 40% das votações nominais selecionadas aparecem no gráfico (ausência e abstenção não são votos válidos e obstrução é considerada equivalente ao voto "não"). Com isso, asseguramos que a pontuação média de cada deputado realmente reflita seu padrão de votação.

### Classificação Temática
Todas as votações passaram por uma triagem temática e uma etapa de classificação, realizada manualmente ou com assistência de inteligência artificial generativa, sempre com revisão e validação final humana. Para definir como classificar cada votação, escolhendo uma das seis tags possíveis, utilizamos como indício inicial a orientação das bancadas partidárias nas pontas do espectro político, mas a decisão final foi sempre baseada no teor da proposta (ementa). 

Foram considerados dois eixos temáticos:

**1. Eixo Econômico (Horizontal - x)**

Separa visões sobre o papel do Estado na economia.
* **Esquerda:** votos a favor de maior intervenção estatal, regulação de mercados, programas sociais robustos, leis trabalhistas protetivas e aumento de investimentos públicos.
* **Liberal:** votos a favor de privatizações, redução de impostos, desburocratização, flexibilização de leis trabalhistas e livre mercado.

**2. Eixo Costumes e Outros Temas (Vertical - y)**

Trata de valores sociais, meio ambiente, justiça, segurança pública, liberdades individuais e outros temas sem relação direta com a área econômica.
* **Progressista:** votos alinhados à defesa de direitos de minorias, preservação ambiental, visões menos punitivistas no direito penal (foco na ressocialização) e ponderação da liberdade de expressão quando em conflito com outros valores constitucionais.
* **Conservador:** votos alinhados à defesa de valores tradicionais, endurecimento de leis penais, flexibilização de regras ambientais e oposição a restrições da liberdade de expressão ou à regulação de redes sociais e outras plataformas digitais.

**Importante:** a classificação de uma pauta indica apenas a direção e o sentido para onde o voto "sim" empurra o deputado no gráfico ("liberal" empurra para a direita e "esquerda" empurra no sentido oposto, enquanto "conservador" empurra para cima e "progressista" para baixo). Isso não significa que toda proposta seja uma representação fiel da visão de mundo expressa pela tag de classificação.

Alguns exemplos: um projeto da área econômica, classificado como "esquerda" ou "liberal", pode ter recebido votos favoráveis até de parlamentares de centro. Um projeto classificado como "conservador" pode ter recebido votos contrários apenas do partido mais progressista, enquanto outra pauta com a mesma classificação pode ter enfrentado resistência de quase toda a Câmara, exceto do partido mais conservador. 

O que define a intensidade da pontuação de cada votação, isto é, o quanto ela leva cada deputado para a esquerda, para a direita, para cima ou para baixo é o critério do tamanho da dissidência, explicado adiante.                         

Além disso, a intenção das votações é considerada na escolha da tag. Se a Câmara vota um requerimento de retirada de pauta de um projeto com viés progressista, o voto "sim" rende pontos de conservadorismo. Já na votação final do projeto, o voto "sim" rende pontos de progressismo.


### Categorias Especiais (inclassificável e moderado)
Algumas votações não cabem na divisão ideológica tradicional e recebem tratamentos específicos:
* **Inclassificável:** são votações cujo padrão torna a classificação ideológica inviável. Geralmente envolvem regras internas, pautas simbólicas ou corporativistas. Aqui, a divisão não é entre esquerda e direita, mas entre defensores e opositores de privilégios ou interesses corporativos (do Legislativo e do Judiciário, por exemplo).
* **Moderado:** esse rótulo é escolhido quando as pontas do espectro político votam juntas contra o centro. Exemplo: deputados de esquerda votam contra uma pauta moderada porque a avaliam como excessivamente liberal, enquanto a direita também vota contra, mas por considerá-la excessivamente intervencionista.

### O Cálculo da Pontuação (Score)
A posição de cada ponto no gráfico não é uma média simples. Utilizamos um modelo matemático de pesos por dissidência, já que votar contra a maioria exige mais convicção e gera mais diferenciação do que segui-la.

Na prática, funciona assim: imagine uma votação classificada com a tag "esquerda" em que 90% do quórum votou "sim" e apenas 10% votou "não". Quem votou "não" (a minoria liberal) recebe uma pontuação alta para a direita (+9), pois marcou posição, diferenciando-se dos demais. Já quem votou "sim" (a maioria) recebe uma pontuação pequena para a esquerda (-1), pois foi um voto de consenso, que não marca uma posição firme à esquerda.

Além disso, uma camada de pós-processamento identifica votos de "centro" e votos de "polo" nas pautas classificadas como moderadas. Se o deputado vota com o centro, sua pontuação tende a zero naquele projeto. Se pertence a um dos polos, segue-se o mesmo critério da dissidência, mas o sinal varia de acordo com o polo identificado (sinal negativo para a esquerda e sinal positivo para a direita).

Ao final, cada deputado ganha um score pela média ponderada de suas votações válidas e os scores são normalizados para caberem na escala de -10 a +10 em ambos os eixos.
### Os 7 Grupos (Clusters)
As cores padrão do gráfico representam 7 grupos de deputados, identificados por um algoritmo de inteligência artificial (K-means++). Esse algoritmo é agnóstico, ou seja, ele não sabe o que é direita ou esquerda. Ele apenas analisa o padrão matemático de como cada deputado votou em centenas de projetos (inclusive os inclassificáveis, que não entram no cálculo ideológico, mas são importantes para a diferenciação em clusters, ao capturar nuances) e agrupa aqueles que votam de forma semelhante entre si. 

Embora a escolha do número de clusters seja flexível, a divisão em 7 grupos foi a que melhor representou a realidade política atual, combinando critérios estatísticos com a análise da Ciência Política sobre a organização do Congresso.
            ''', className="markdown-texto", link_target="_blank")

        ], width=12, lg=8)
    ], justify="center")
], fluid=True, className="py-5 px-4")