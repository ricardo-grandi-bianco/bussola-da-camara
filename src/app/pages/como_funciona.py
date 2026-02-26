# Página explicando funcionamento da Bússola

# Importações
import dash_bootstrap_components as dbc
from dash import html, dcc

# Layout da página
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Como Funciona", className="display-4 text-primary fw-bold mb-4"),
            dcc.Markdown('''
                
### O que a Bússola da Câmara mostra?

A Bússola da Câmara posiciona os deputados federais da 57ª legislatura (2022-2026) em um mapa ideológico. A posição de cada deputado(a) não é baseada em opiniões declaradas, mas sim em **como ele ou ela votou** nas propostas apresentadas no Plenário, como projetos de lei ou de emenda constitucional (PEC).

> **Observação:** você pode não encontrar alguns nomes, ou encontrar outros que não são mais parlamentares. Isso acontece porque incluímos apenas os deputados eleitos em 2022 que deram votos válidos em pelo menos **40% das votações analisadas**. Por isso, suplentes que assumiram o cargo recentemente podem não estar no gráfico, enquanto deputados que se licenciaram (para assumir ministérios, por exemplo) ainda podem aparecer se tiverem atingido essa taxa mínima de participação.

### Entendendo os Eixos

Cada ponto no gráfico representa um deputado. A localização é definida por uma pontuação que vai de **-10 a +10** em dois eixos diferentes:

* **Eixo Horizontal (Economia):** mede o posicionamento em temas como impostos, programas sociais e regulação de mercado.
    * **Para a esquerda (próximo de -10):** tendência a votar por maior intervenção do Estado na economia.
    * **Para a direita (próximo de +10):** tendência a votar de forma liberal, favorecendo o livre mercado e a iniciativa privada.
* **Eixo Vertical (Costumes e Outros):** mede o posicionamento em temas como meio ambiente, leis penais e pautas morais.
    * **Para cima (próximo de +10):** votos alinhados a pautas conservadoras.
    * **Para baixo (próximo de -10):** votos alinhados a pautas progressistas.

### O que significam as cores?

As cores padrão dividem os deputados em **7 grupos distintos**, gerados por um modelo matemático (para mais informações, veja as páginas *Descobertas* e *Metodologia*).

Se preferir, você pode visualizar as cores por partido ou federação, selecionando a opção **Colorir por: Partidos** no menu lateral.

### Como encontrar um deputado e filtrar os dados

Você tem várias formas de explorar os dados:

* **Busca direta:** digite o nome do(a) parlamentar na caixa de busca "Buscar Deputado(a)".
* **Filtros:** selecione um partido ou uma UF específica (um estado ou o Distrito Federal) para ver apenas seus deputados no gráfico. *Dica: dê um duplo clique rápido na legenda colorida para isolar um grupo ou partido.*
* **No gráfico:** passe o mouse sobre qualquer ponto para ver o nome do(a) deputado(a) e a sua pontuação. Ao clicar no ponto, ele ficará destacado e um **cartão de perfil** aparecerá no canto inferior esquerdo com a foto e os dados detalhados.

### Navegando pelo mapa

A ferramenta é interativa e permite análise detalhada:

* **Zoom e Movimento:** use a rolagem do mouse (scroll) para aproximar ou afastar. Clique e arraste o fundo do gráfico para mover a visualização.
* **Lupa (canto superior direito):** clique neste ícone para selecionar com o mouse uma área específica do gráfico que você deseja ampliar.
* **Casinha (canto superior direito):** ajusta a tela automaticamente para retornar ao zoom original.
* **Limpar Filtros:** botão essencial para "resetar" a Bússola. Ele remove todas as seleções de busca, restaurando o gráfico ao estado padrão, em que aparecem todos os deputados avaliados.
                         
### Experiência de navegação
                         
Para que você tenha a melhor experiência de navegação na Bússola da Câmara, recomendamos abrir o site no computador. Se utilizar o celular, os filtros funcionam melhor com o apareho na vertical. Já para a visualização do gráfico, o ideal é utilizá-lo na horizontal. 
            ''', className="markdown-texto", link_target="_blank")

        ], width=12, lg=8)
    ], justify="center")
], fluid=True, className="py-5 px-4")