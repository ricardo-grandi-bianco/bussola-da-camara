# Página principal com gráfico interativo e filtros

# Importações
import dash
from dash import dcc, html, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "final" / "bussola_dash_producao.parquet"

# Leitura dos dados
try:
    df = pd.read_parquet(DATA_PATH)
except:
    df = pd.DataFrame()

# Mapeamento de Cores
CORES_CLUSTER = {
    '0': '#17ea39', '1': '#1ebfec', '2': '#A7194B', '3': '#e7c2c0',
    '4': '#FFCD00', '5': '#FE2712', '6': '#3E01A4'
}

NOMES_CLUSTER = {
    '0': 'Oposição Conservadora', '1': 'Centro Eclético', '2': 'Esquerda Ideológica',
    '3': 'Centrão Governista', '4': 'Progressistas Independentes',
    '5': 'Esquerda Governista', '6': 'Direita Tradicional'
}

CORES_PARTIDO = {
    'PT': '#CE3942', 'PV': '#CE3942', 'PCdoB': '#CE3942', 'PL': '#295AA5',
    'PSOL': '#4C0E71', 'REDE': '#4C0E71', 'UNIAO':'#33BFEF',
    'PP': '#72BADE', 'PSD': '#F5CF27', 'MDB': '#6AC54E',
    'PSDB': '#2A15D2', 'CIDADANIA': '#2A15D2', 'PRD': '#2B8552', 'SOLIDARIEDADE': '#2B8552',
    'NOVO': '#EB732A', 'PDT': '#D82355', 'AVANTE': '#DE683C',
    'PODE': '#4CAF35', 'PSB': '#FFC600', 'REPUBLICANOS': "#FFFFFF"
}
COR_PARTIDO_DEFAULT = '#999999'

# Ordem Lógica dos Grupos (Esquerda -> Direita)
ORDEM_VISUAL_CLUSTERS = [
    'Esquerda Ideológica',
    'Esquerda Governista',
    'Progressistas Independentes',
    'Centrão Governista',
    'Centro Eclético',
    'Direita Tradicional',
    'Oposição Conservadora'
]

# Mapeamento de Federações Partidárias
MAPA_FEDERACOES = {
    # Federação Brasil da Esperança
    'PT': 'PT/PV/PCdoB', 'PV': 'PT/PV/PCdoB', 'PCdoB': 'PT/PV/PCdoB',
    # Federação PSOL-REDE
    'PSOL': 'PSOL/REDE', 'REDE': 'PSOL/REDE',
    # Federação PSDB-Cidadania
    'PSDB': 'PSDB/CIDADANIA', 'CIDADANIA': 'PSDB/CIDADANIA',
    # Federação PRD-Solidariedade
    'PRD': 'PRD/SOLIDARIEDADE', 'SOLIDARIEDADE': 'PRD/SOLIDARIEDADE'
}

# Tratamento inicial dos dados
if not df.empty:
    df['cluster'] = df['cluster'].astype(str)
    df['deputado_siglaPartido'] = df['deputado_siglaPartido'].astype(str).str.strip()
    df['deputado_siglaPartido'] = df['deputado_siglaPartido'].apply(lambda x: 'UNIAO' if 'UNI' in x else x)
    mudancas_partido = {
        'Tiririca': 'PSD',
        'Luiz Lima': 'NOVO'
    }
    for deputado, novo_partido in mudancas_partido.items():
        df.loc[df['deputado_nome'] == deputado, 'deputado_siglaPartido'] = novo_partido
    df['label_busca'] = df['deputado_nome'] + ' (' + df['deputado_siglaPartido'] + '-' + df['deputado_siglaUf'] + ')'

# Geração de listas para os filtros
lista_deputados = df[['deputado_id', 'label_busca']].sort_values('label_busca').to_dict('records')
lista_partidos = sorted(df['deputado_siglaPartido'].unique())
lista_estados = sorted(df['deputado_siglaUf'].unique())

# Layout
layout = dbc.Row([
    dcc.Store(id='browser-size', data={'width': 1200, 'height': 800}),
    html.Button(id='btn-resize-fantasma', style={'display': 'none'}), # O nosso espião de rotação!
    # Coluna Esquerda: Filtros e Card
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.Label("Colorir por:", className="fw-bold"),
                dbc.RadioItems(
                    id='radio-color-mode',
                    options=[{'label': 'Grupos', 'value': 'cluster'}, {'label': 'Partidos', 'value': 'partido'}],
                    value='cluster',
                    inline=True,
                    className="mb-3"
                ),
                html.Label("Buscar Deputado(a):", className="fw-bold"),
                dcc.Dropdown(
                    id='dropdown-deputado',
                    options=[{'label': d['label_busca'], 'value': d['deputado_id']} for d in lista_deputados],
                    placeholder="Digite nome...",
                    className="mb-3", clearable=True
                ),
                html.Label("Filtrar por Partido:", className="fw-bold"),
                dcc.Dropdown(
                    id='dropdown-partido',
                    options=[{'label': p, 'value': p} for p in lista_partidos],
                    placeholder="Todos os partidos",
                    className="mb-3", clearable=True
                ),
                html.Label("Filtrar por Estado:", className="fw-bold"),
                dcc.Dropdown(
                    id='dropdown-estado',
                    options=[{'label': e, 'value': e} for e in lista_estados],
                    placeholder="Todos os estados",
                    className="mb-3", clearable=True
                ),
                dbc.Button("Limpar Filtros", id="btn-reset", color="secondary", outline=True, size="sm", className="w-100")
            ])
        ], className="mb-4 shadow-sm"),
        html.Div(id='card-deputado-container')
    ], width=12, lg=3, className="mb-4"),

    # Coluna Direita: Gráfico
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(
                    id='grafico-principal',
                    style={'height': '85vh', 'minHeight': '550px'},
                    config={'displayModeBar': True, 'scrollZoom': True, 'doubleClick': 'reset'},
                    clear_on_unhover=True
                )
            ], className="p-1")
        ], className="shadow-sm h-100")
    ], width=12, lg=9)
])

# Lógica de tela PC vs. Mobile
dash.clientside_callback(
    """
    function(id_trigger, n_clicks) {
        if (!window.monitor_de_rotacao) {
            window.addEventListener('resize', function() {
                var btn = document.getElementById('btn-resize-fantasma');
                if (btn) { btn.click(); }
            });
            window.monitor_de_rotacao = true;
        }
        return {width: window.innerWidth, height: window.innerHeight};
    }
    """,
    Output('browser-size', 'data'),
    [Input('browser-size', 'id'), Input('btn-resize-fantasma', 'n_clicks')]
)

# Callbacks
@callback(
    [Output('grafico-principal', 'figure'),
     Output('card-deputado-container', 'children'),
     Output('dropdown-deputado', 'value'),
     Output('dropdown-partido', 'value'),
     Output('dropdown-estado', 'value')],
    [Input('radio-color-mode', 'value'),
     Input('dropdown-deputado', 'value'),
     Input('dropdown-partido', 'value'),
     Input('dropdown-estado', 'value'),
     Input('grafico-principal', 'clickData'),
     Input('btn-reset', 'n_clicks'),
     Input('browser-size', 'data')]
)
def update_dashboard(color_mode, dep_selecionado, partido_selecionado, estado_selecionado, click_data, n_reset, browser_data):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Responsividade da tela
    largura_tela = browser_data.get('width', 1200) if browser_data else 1200
    
    if largura_tela < 600:
        fator_tamanho = 0.6  
        fonte_legenda = 9
        fonte_anotacoes = 10  
        travar_quadrado = True
    elif largura_tela < 992:
        fator_tamanho = 0.75 
        fonte_legenda = 10
        fonte_anotacoes = 12
        travar_quadrado = False
    else:
        fator_tamanho = 1.0   
        fonte_legenda = 11
        fonte_anotacoes = 14
        travar_quadrado = False

    # Lógica de Reset
    if trigger_id == 'btn-reset':
        dep_selecionado = None
        partido_selecionado = None
        estado_selecionado = None

    # Seleção via clique
    if trigger_id == 'grafico-principal' and click_data:
        dep_selecionado = click_data['points'][0]['customdata'][0]
    
    dff = df.copy()

    # Aplicação de filtros
    if partido_selecionado:
        dff = dff[dff['deputado_siglaPartido'] == partido_selecionado]
    if estado_selecionado:
        dff = dff[dff['deputado_siglaUf'] == estado_selecionado]

    if color_mode == 'partido':
        dff['legenda'] = dff['deputado_siglaPartido'].replace(MAPA_FEDERACOES)
        cores_mapa = CORES_PARTIDO.copy()
        cores_mapa.update({'PT/PV/PCdoB': CORES_PARTIDO['PT'], 'PSOL/REDE': CORES_PARTIDO['PSOL'], 'PSDB/CIDADANIA': CORES_PARTIDO['PSDB'], 'PRD/SOLIDARIEDADE': CORES_PARTIDO['PRD']})
        dff['cor_final'] = dff['deputado_siglaPartido'].map(CORES_PARTIDO).fillna(COR_PARTIDO_DEFAULT)
    else:
        dff['cor_final'] = dff['cluster'].map(CORES_CLUSTER)
        dff['legenda'] = dff['cluster'].map(NOMES_CLUSTER)
        cores_mapa = {v: CORES_CLUSTER[k] for k, v in NOMES_CLUSTER.items()}

    # Ajuste dos pontos
    dff['opacity'] = 0.9
    dff['size'] = 9 * fator_tamanho          
    dff['line_width'] = 1 * fator_tamanho    
    dff['line_color'] = 'DarkSlateGrey'
    
    # Card
    card_content = html.Div([
        html.Div([
            html.Img(src="/assets/Logo.jpeg", style={'width': '80%', 'maxWidth': '250px', 'marginBottom': '20px'}),
        ], className="text-center opacity-75") 
    ])

    if dep_selecionado:
        if dep_selecionado in dff['deputado_id'].values:
            dff.loc[dff['deputado_id'] != dep_selecionado, 'opacity'] = 0.1 
            mask = dff['deputado_id'] == dep_selecionado
            dff.loc[mask, 'opacity'] = 1.0
            
            dff.loc[mask, 'size'] = 15 * fator_tamanho       
            dff.loc[mask, 'line_width'] = 2 * fator_tamanho  
            dff.loc[mask, 'line_color'] = '#000000'

            row = df[df['deputado_id'] == dep_selecionado].iloc[0]
            cor_tribo = CORES_CLUSTER.get(str(row['cluster']), '#333')
            nome_tribo = NOMES_CLUSTER.get(str(row['cluster']), 'Desconhecido')

            card_content = dbc.Card([
                dbc.Row([
                    dbc.Col(dbc.CardImg(src=row['deputado_urlFoto'], className="img-fluid rounded-start", style={'height': '100%', 'objectFit': 'contain', 'backgroundColor': '#f8f9fa', 'maxHeight': '230px', 'minHeight': '230px'}), width=6, className="d-flex align-items-center justify-content-center bg-light p-0"),
                    dbc.Col(dbc.CardBody([
                            html.H5(f"{row['deputado_nome']}", className="card-title mb-0", style={'fontSize': '1rem', 'fontWeight': 'bold'}),
                            html.P(f"{row['deputado_siglaPartido']} - {row['deputado_siglaUf']}", className="text-muted small mb-2"),
                            html.Hr(className="my-2"),
                            html.Div([html.Span("Grupo:", className="small fw-bold d-block text-muted"), html.Span(nome_tribo, style={'color': cor_tribo, 'fontWeight': 'bold', 'fontSize': '0.85rem'})], className="mb-2"),
                            dbc.Row([
                                dbc.Col([html.Small("Economia", className="text-muted d-block", style={'fontSize': '0.75rem'}), html.Span(f"{row['x_final']:.2f}", className="fw-bold", style={'fontSize': '1rem'})], width=6),
                                dbc.Col([html.Small("Outros temas", className="text-muted d-block", style={'fontSize': '0.75rem'}), html.Span(f"{row['y_final']:.2f}", className="fw-bold", style={'fontSize': '1rem'})], width=6, className="text-center p-0"),
                            ], className="g-0")
                        ], className="p-3"), width=6),
                ], className="g-0 align-items-center") 
            ], className="shadow-lg border-primary fade-in", style={'overflow': 'hidden'})

    # Texto para hover
    dff['hover_text'] = ("<b>" + dff['deputado_nome'] + "</b> (" + dff['deputado_siglaPartido'] + "-" + dff['deputado_siglaUf'] + ")<br>Economia: " + dff['x_final'].map('{:,.2f}'.format) + "<br>Costumes/Outros: " + dff['y_final'].map('{:,.2f}'.format))

    # Plotly base
    fig = px.scatter(
        dff, x='x_final', y='y_final', color='legenda', color_discrete_map=cores_mapa, hover_name=None, hover_data=None,
        custom_data=['deputado_id', 'hover_text', 'size', 'opacity', 'line_width', 'line_color'], category_orders={'legenda': ORDEM_VISUAL_CLUSTERS}    
    )

    fig.update_traces(hovertemplate="%{customdata[1]}<extra></extra>", mode='markers')

    for trace in fig.data:
        if trace.customdata is not None:
            trace.marker.size = trace.customdata[:, 2].astype(float)
            trace.marker.opacity = trace.customdata[:, 3].astype(float)
            trace.marker.line.width = trace.customdata[:, 4].astype(float)
            trace.marker.line.color = trace.customdata[:, 5]

    data_list = list(fig.data)
    centrao_trace = None
    for trace in data_list:
        if trace.name in ORDEM_VISUAL_CLUSTERS: trace.legendrank = ORDEM_VISUAL_CLUSTERS.index(trace.name)
        if trace.name == 'Centrão Governista': centrao_trace = trace
    if centrao_trace:
        data_list.remove(centrao_trace) 
        data_list.append(centrao_trace) 
    fig.data = tuple(data_list)

    # Layout responsivo
    fig.update_xaxes(range=[-12.5, 12.5], autorange=False, zeroline=False, showgrid=False, showticklabels=False, title="")
    fig.update_yaxes(range=[-12.5, 12.5], autorange=False, zeroline=False, showgrid=False, showticklabels=False, title="",
                     scaleanchor="x" if travar_quadrado else None, scaleratio=1 if travar_quadrado else None)

    fig.update_layout(
        uirevision='locked', template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20), dragmode='pan',     
        modebar=dict(orientation='v', bgcolor='#FFFFFF', remove=['lasso2d', 'select2d', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage', 'zoomIn2d', 'zoomOut2d', 'toggleSpikelines']),
        legend=dict(
            orientation="v", yanchor="bottom", y=0, xanchor="right", x=0.99,
            bgcolor="#FFFFFF", bordercolor="#ddd", borderwidth=1, title_text="", itemsizing='constant', font=dict(size=fonte_legenda)
        ) 
    )

    fig.add_hline(y=0, line_width=1.5, line_dash="solid", line_color="#ddd", layer="below")
    fig.add_vline(x=0, line_width=1.5, line_dash="solid", line_color="#ddd", layer="below")

    fig.add_scatter(x=[6], y=[-0.6], text=["↔ Economia"], mode="text", textposition="middle center", textfont=dict(size=max(8, fonte_anotacoes-2), color="#ccc"), showlegend=False, hoverinfo="skip")
    fig.add_annotation(x=0.3, y=-8, text="Costumes/Outros ↔", textangle=-90, showarrow=False, font=dict(size=max(8, fonte_anotacoes-2), color="#ccc"))
    fig.add_scatter(x=[-9], y=[-12], text=["Dados atualizados até 01/02/2026"], mode="text", textposition="middle center", textfont=dict(size=max(8, fonte_anotacoes-4), color="#ccc"), showlegend=False, hoverinfo="skip")

    fig.add_scatter(x=[-12], y=[-1.8], text=["<b>← ESQUERDA</b>"], mode="text", textposition="middle right", textfont=dict(size=fonte_anotacoes, color="#CE3942"), showlegend=False, hoverinfo="skip")
    fig.add_scatter(x=[12], y=[1.8], text=["<b>LIBERAL →</b>"], mode="text", textposition="middle left", textfont=dict(size=fonte_anotacoes, color="#418ACB"), showlegend=False, hoverinfo="skip")
    fig.add_scatter(x=[2.4], y=[12], text=["<b>CONSERVADOR ↑</b>"], mode="text", textposition="bottom center", textfont=dict(size=fonte_anotacoes, color="#3E01A4"), showlegend=False, hoverinfo="skip")
    fig.add_scatter(x=[-2.4], y=[-12], text=["<b>PROGRESSISTA ↓</b>"], mode="text", textposition="top center", textfont=dict(size=fonte_anotacoes, color="#F7C71C"), showlegend=False, hoverinfo="skip")
    
    return fig, card_content, dep_selecionado, partido_selecionado, estado_selecionado