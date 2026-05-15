# Página explicando as principais descobertas e os clusters

# Importações
import dash_bootstrap_components as dbc
from dash import html, dcc

# Layout da página
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Descobertas", className="display-4 text-primary fw-bold mb-4"),
            
            # Bloco de texto 1
            dcc.Markdown('''
### Grupos 

Os deputados foram divididos em 7 grupos segundo seu padrão de votação, utilizando um modelo de *machine learning*. São eles:
- **Esquerda Ideológica**: formada por 15 deputados, incluindo toda a bancada do PSOL. Fiel às pautas da esquerda, o grupo apoia o Governo na maioria das votações, mas tende a se opor à base petista quando ela faz acordos ou concessões ao centro.
- **Esquerda Governista**: são 84 deputados, majoritariamente da Federação PT/PV/PCdoB. Formam o núcleo duro do Governo Lula na Câmara. Embora mantenham forte identidade de esquerda, atuam com pragmatismo, negociando com o centro ou a oposição para aprovar pautas prioritárias.
- **Progressistas Independentes**: a maioria dos 41 deputados desse grupo pertence a partidos de centro-esquerda, como PDT e PSB. Posicionam-se no campo progressista, mas com perfis variados: de sindicalistas tradicionais a jovens ativistas da educação ou da causa animal, por exemplo. É o segundo grupo mais governista, mas alguns integrantes demonstram independência e visões mais próxmias ao centro.
- **Centrão Governista**: maior grupo da Câmara, com 112 deputados. Vota com o Governo em cerca de 83% das ocasiões, mas não por alinhamento ideológico, e sim por negociações políticas, frequentemente envolvendo emendas. Reúne parlamentares de legendas como Republicanos, PP, União Brasil, PSD e MDB.
- **Centro Eclético**: como o nome sugere, é o grupos mais heterogêneo. Seus 101 deputados se dividem entre parlamentares com visão de centro, lideranças partidárias de legendas como MDB, PSDB e Podemos, figuras midiáticas, integrantes do centrão mais independentes e políticos municipalistas. O que os une é o perfil de votação moderado ou difuso, afastando-se tanto do Governo quanto da oposição conservadora.
- **Direita Tradicional**: primeiro grupo claramente de oposição, com governismo médio de 42%. É composto por 55 deputados de centro-direita e direita, vindos de siglas como PL, União Brasil e PP. Também apresenta um perfil variado, mas abriga muitos representantes de setores tradicionais, como o agronegócio. Embora conservadores, não adotam uma postura intransigente. Alguns ocupam espaços de liderança na Casa e negociam pautas específicas com o Governo.
- **Oposição Conservadora**: é o núcleo duro da oposição, com 87 deputados. Formado majoritariamente pelo PL, mas também pela bancada do Novo e por outros parlamentares de direita, possui índice de governismo inferior a 24%. É o grupo mais à direita da Câmara, combinando forte liberalismo econômico com posições conservadoras nos costumes e em outros temas sociais.     

Veja na imagem abaixo as posições médias de cada grupo.
            ''', className="markdown-texto", link_target="_blank"),

            # Imagem 1
            html.Div([
                html.Img(
                    src="/assets/imagem 1.png", 
                    className="img-fluid rounded shadow-sm",
                    style={'maxHeight': '500px'}
                ),
                html.Small("Dados: Câmara dos Deputados/ Bússola da Câmara", className="text-muted d-block mt-2")
            ], className="text-center my-4"),

            # Bloco de texto 2
            dcc.Markdown('''
**Importante**: como todo modelo matemático, a Bússola da Câmara é uma simplificação da realidade. Por isso, a divisão em dois eixos e 7 grupos pode não refletir pequenas nuances e particiularidades do comportamento de alguns deputados. Ainda assim, ela é muito útil para entender os padrões gerais de votação dos parlamentares e seus posicionamentos.  

### Deputado médio: distância do governo e da oposição
                         
A distância entre o deputado médio (parlamentar "fictício" que representa o posicionamento médio de todos os deputados) e o núcleo do Governo é de 9,5 unidades. Já em relação ao núcleo da oposição, a distância é de 11,9 unidades. Isso mostra que a Câmara apresenta uma média ligeiramente mais governista, porém relativamente distante de ambos os grupos.
                         
Separando por eixos, o deputado médio é cerca de 4,4 pontos mais liberal e 8,4 pontos mais conservador do que a esquerda governista. Já a oposição conservadora fica 8 pontos para a direita e 8,8 pontos para cima em relação à média da Casa.   
            ''', className="markdown-texto", link_target="_blank"),

            # Imagem 2
            html.Div([
                html.Img(src="/assets/imagem 2.png", className="img-fluid rounded shadow-sm"),
                html.Small("Dados: Câmara dos Deputados/ Bússola da Câmara", className="text-muted d-block mt-2")
            ], className="text-center my-4"),

            # Bloco de texto 3
            dcc.Markdown('''
### Partidos
                         
O PSOL é o partido mais à esquerda e progressista. Já na outra ponta, o Novo é o que apresenta, em média, as votações mais liberais e conservadoras. Veja as posições médias de cada partido ou federação partidária abaixo.
            ''', className="markdown-texto", link_target="_blank"),

            # Imagem 3
            html.Div([
                html.Img(src="/assets/imagem 3.png", className="img-fluid rounded shadow-sm"),
                html.Small("Dados: Câmara dos Deputados/ Bússola da Câmara", className="text-muted d-block mt-2")
            ], className="text-center my-4"),

 # Bloco de texto 4
            dcc.Markdown('''
Há diferentes níveis de coesão partidária. Alguns partidos e federações partidárias possuem uma ideologia bem definida e seus membros votam de forma alinhada (alta coesão), enquanto outros abrigam deputados com padões de votação bastante variados (alta dispersão).
Em ordem decrescente de coesão, temos:
- **Alta coesão**: PT/PV/PCdoB, PSOL/Rede, Novo, PDT, PSB.
- **Média coesão**: Avante, PL, Republicanos, MDB.
- **Baixa coesão**: PSDB/Cidadania, PSD, Podemos, PP/União Brasil, PRD/Solidariedade.

No gráfico, isso é visível ao filtrar por partido. Legendas de alta coesão aparecem como pontos concentrados, enquanto as de baixa coesão mostram pontos espalhados pelo mapa.
                          
**Observação**: o partido Missão não entrou no cálculo de coesão, pois possui apenas um deputado federal. 
\n
\n

### Outras descobertas e curiosidades:
- **Gênero**: embora a diferença estatística seja pequena, parlamentares do gênero feminino ficam, em média, 0,4 ponto mais à esquerda e são 1,6 ponto mais progressistas do que seus colegas do gênero masculino.
            ''', className="markdown-texto", link_target="_blank"),

            # Imagem 4
            html.Div([
                html.Img(
                    src="/assets/imagem 4.png", 
                    className="img-fluid rounded shadow-sm",
                    style={'maxHeight': '500px'} 
                ),
                html.Small("Dados: Câmara dos Deputados/ Bússola da Câmara", className="text-muted d-block mt-2")
            ], className="text-center my-4"), 

            # Bloco de texto 5
            dcc.Markdown('''
- **Esquerda 🤝 Progressismo x Liberalismo econômico 🤝 Conservadorismo**: na Câmara brasileira atual, as posições progressistas nos costumes tendem a caminhar junto com o intervencionismo na economia e o liberalismo econômico anda de mãos dadas com o conservadorismo moral. Para observar esse fenômeno no gráfico, basta notar que o canto superior esquerdo (estatismo conservador) e o inferior direito (liberalismo progressista) estão praticamente vazios.
            ''', className="markdown-texto", link_target="_blank"),

            # Imagem 5
            html.Div([
                html.Img(src="/assets/imagem 5.png", className="img-fluid rounded shadow-sm"),
                html.Small("Dados: Câmara dos Deputados/ Bússola da Câmara", className="text-muted d-block mt-2")
            ], className="text-center my-4")

                    ], width=12, lg=8)
    ], justify="center")
], fluid=True, className="py-5 px-4")