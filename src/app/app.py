# Servidor principal do app e layout

# Importações
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pathlib import Path

# Importação das páginas
from pages import home, como_funciona, descobertas, metodologia, quem_somos

# Configuração de caminhos
BASE_DIR = Path(__file__).parent
ASSETS_PATH = BASE_DIR.parent.parent / "assets"

# Inicialização do App
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
    title="Bússola da Câmara",
    assets_folder=str(ASSETS_PATH)
)
server = app.server

# Componentes da barra de navegação
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", id="nav-home")),
        dbc.NavItem(dbc.NavLink("Como Funciona", href="/como-funciona", id="nav-como-funciona")),
        dbc.NavItem(dbc.NavLink("Descobertas", href="/descobertas", id="nav-descobertas")),
        dbc.NavItem(dbc.NavLink("Metodologia", href="/metodologia", id="nav-metodologia")),
        dbc.NavItem(dbc.NavLink("Quem Somos", href="/quem-somos", id="nav-quem-somos")),
    ],
    brand="BÚSSOLA DA CÂMARA",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
    sticky="top",
    className="mb-4"
)

# Callback para destacar o link ativo na barra de navegação
@app.callback(
    [Output("nav-home", "active"),
     Output("nav-como-funciona", "active"),
     Output("nav-descobertas", "active"),
     Output("nav-metodologia", "active"),
     Output("nav-quem-somos", "active")],
    [Input("url", "pathname")]
)
def toggle_active_links(pathname):
    if pathname is None:
        return True, False, False, False, False
    
    return (
        pathname == "/" or pathname == "/home",
        pathname == "/como-funciona",
        pathname == "/descobertas",
        pathname == "/metodologia",
        pathname == "/quem-somos"
    )

# Layout Principal
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', fluid=True, className="px-4")
])

# Callback de Navegação
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/home':
        return home.layout
    elif pathname == '/como-funciona':
        return como_funciona.layout
    elif pathname == '/descobertas':
        return descobertas.layout
    elif pathname == '/metodologia':
        return metodologia.layout
    elif pathname == '/quem-somos':
        return quem_somos.layout
    else:
        return html.H1("404: Página não encontrada", className="text-danger text-center mt-5")

if __name__ == '__main__':
    app.run(debug=False)