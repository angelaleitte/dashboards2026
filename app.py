"""
Painéis Angela Leitte — Multi-páginas estilo Power BI
paineis.angelaleitte.com.br
"""
import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random

# --- Dados fictícios ---
def dados_vendas():
    random.seed(42)
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    return pd.DataFrame({
        'Mês': meses,
        'Vendas': [random.randint(85, 160) for _ in range(12)],
        'Meta': [120] * 12,
        'Região': random.choices(['Sul', 'Sudeste', 'Norte', 'Nordeste'], k=12)
    })

def dados_operacoes():
    random.seed(123)
    categorias = ['Entregas', 'Suporte', 'Vendas', 'Marketing', 'TI', 'RH']
    return pd.DataFrame({
        'Área': categorias,
        'Atividades': [random.randint(50, 200) for _ in range(6)],
        'Concluído %': [random.randint(75, 99) for _ in range(6)]
    })

def serie_temporal(periodos=90):
    random.seed(456)
    datas = pd.date_range(start='2024-01-01', periods=periodos, freq='D')
    base = 100
    vals = [base]
    for _ in range(periodos - 1):
        base = max(50, base + random.gauss(2, 8))
        vals.append(round(base, 1))
    return pd.DataFrame({'Data': datas, 'Valor': vals})

# --- App ---
app = dash.Dash(__name__, title="Painéis Angela Leitte", update_title="Carregando...", suppress_callback_exceptions=True)
server = app.server

# Tema gráficos (estilo Power BI)
THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Segoe UI, sans-serif", color="#252423"),
    margin=dict(t=24, b=24, l=40, r=24),
    xaxis=dict(showgrid=True, gridcolor="#edebe9", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#edebe9", zeroline=False),
    colorway=["#0078d4", "#107c10", "#d83b01", "#8764b8", "#00b7c3", "#ff8c00"],
)

# --- Componentes reutilizáveis ---
def navbar(pathname):
    return html.Header(className="navbar", children=[
        html.A("Painéis Angela Leitte", href="/", className="navbar-brand"),
        html.Nav(className="navbar-nav", children=[
            html.A("Início", href="/", className="nav-link" + (" active" if pathname == "/" else "")),
        ]),
    ])

def link_card(title, href, description, icon, disabled=False):
    if disabled:
        return html.Div(className="dashboard-card disabled", children=[
            html.Div(className="card-icon placeholder", children="📊"),
            html.H3(title, className="card-title"),
            html.P(description or "Em breve", className="card-desc"),
            html.Span("Em breve", className="card-badge"),
        ])
    return html.A(className="dashboard-card", href=href, children=[
        html.Div(className="card-icon", children=icon),
        html.H3(title, className="card-title"),
        html.P(description or "", className="card-desc"),
        html.Span("Abrir →", className="card-link"),
    ])

# --- Página inicial ---
def layout_home():
    return html.Div(className="page page-home", children=[
        html.Div(className="home-hero", children=[
            html.H1("Painéis de negócio", className="hero-title"),
            html.P("Escolha um dashboard abaixo. Novos painéis serão adicionados em breve.", className="hero-subtitle"),
        ]),
        html.Div(className="dashboard-grid", children=[
            link_card("Vendas", "/vendas", "Receita, metas e desempenho por período", "📈"),
            link_card("Operações", "/operacoes", "Atividades por área e taxa de conclusão", "⚙️"),
            link_card("Dashboard 3", None, None, None, disabled=True),
            link_card("Dashboard 4", None, None, None, disabled=True),
            link_card("Dashboard 5", None, None, None, disabled=True),
            link_card("Dashboard 6", None, None, None, disabled=True),
        ]),
    ])

# --- Dashboard Vendas ---
def layout_vendas():
    return html.Div(className="page page-dashboard", children=[
        html.Div(className="dashboard-header", children=[
            html.H1("Vendas", className="dashboard-title"),
            html.P("Visão de receita e metas", className="dashboard-subtitle"),
        ]),
        html.Div(className="kpi-row", children=[
            html.Div(className="kpi-card", children=[
                html.Span("Receita total", className="kpi-label"),
                html.Span("R$ 1.428.500", className="kpi-value"),
                html.Span("+12% vs anterior", className="kpi-trend up"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Span("Meta do mês", className="kpi-label"),
                html.Span("94%", className="kpi-value"),
                html.Span("Acima da meta", className="kpi-trend up"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Span("Pedidos", className="kpi-label"),
                html.Span("2.847", className="kpi-value"),
                html.Span("+8%", className="kpi-trend up"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Span("Ticket médio", className="kpi-label"),
                html.Span("R$ 502", className="kpi-value"),
                html.Span("-2%", className="kpi-trend down"),
            ]),
        ]),
        html.Div(className="chart-row", children=[
            html.Div(className="chart-card half", children=[
                html.H3("Vendas por mês", className="chart-title"),
                dcc.Graph(id="vendas-barras", config={"displayModeBar": True, "responsive": True}),
            ]),
            html.Div(className="chart-card half", children=[
                html.H3("Vendas vs Meta", className="chart-title"),
                dcc.Graph(id="vendas-vs-meta", config={"displayModeBar": True, "responsive": True}),
            ]),
        ]),
        html.Div(className="chart-row", children=[
            html.Div(className="chart-card full", children=[
                html.H3("Evolução (série temporal)", className="chart-title"),
                dcc.Graph(id="vendas-linha", config={"displayModeBar": True, "responsive": True}),
            ]),
        ]),
    ])

# --- Dashboard Operações ---
def layout_operacoes():
    return html.Div(className="page page-dashboard", children=[
        html.Div(className="dashboard-header", children=[
            html.H1("Operações", className="dashboard-title"),
            html.P("Atividades por área e desempenho", className="dashboard-subtitle"),
        ]),
        html.Div(className="kpi-row", children=[
            html.Div(className="kpi-card", children=[
                html.Span("Atividades totais", className="kpi-label"),
                html.Span("892", className="kpi-value"),
                html.Span("Este mês", className="kpi-trend"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Span("Conclusão média", className="kpi-label"),
                html.Span("91%", className="kpi-value"),
                html.Span("Acima do target", className="kpi-trend up"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Span("Áreas ativas", className="kpi-label"),
                html.Span("6", className="kpi-value"),
                html.Span("Todas operando", className="kpi-trend"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Span("Pendências", className="kpi-label"),
                html.Span("78", className="kpi-value"),
                html.Span("-15% vs anterior", className="kpi-trend down"),
            ]),
        ]),
        html.Div(className="chart-row", children=[
            html.Div(className="chart-card half", children=[
                html.H3("Atividades por área", className="chart-title"),
                dcc.Graph(id="ops-barras", config={"displayModeBar": True, "responsive": True}),
            ]),
            html.Div(className="chart-card half", children=[
                html.H3("Taxa de conclusão por área", className="chart-title"),
                dcc.Graph(id="ops-gauge", config={"displayModeBar": True, "responsive": True}),
            ]),
        ]),
        html.Div(className="chart-row", children=[
            html.Div(className="chart-card full", children=[
                html.H3("Distribuição de atividades", className="chart-title"),
                dcc.Graph(id="ops-pizza", config={"displayModeBar": True, "responsive": True}),
            ]),
        ]),
    ])

# --- Layout raiz (multi-página) ---
app.layout = html.Div(className="app-root", children=[
    dcc.Location(id="url", refresh=False),
    html.Div(id="navbar-wrap"),
    html.Main(id="page-content", className="main-content"),
])

@callback(
    [Output("page-content", "children"), Output("navbar-wrap", "children")],
    Input("url", "pathname")
)
def render_page(pathname):
    pathname = pathname or "/"
    nav = navbar(pathname)
    if pathname == "/":
        return layout_home(), nav
    if pathname == "/vendas":
        return layout_vendas(), nav
    if pathname == "/operacoes":
        return layout_operacoes(), nav
    return layout_home(), nav

# --- Callbacks gráficos Vendas ---
@callback(Output("vendas-barras", "figure"), Input("url", "pathname"))
def fig_vendas_barras(pathname):
    if pathname != "/vendas":
        return go.Figure()
    df = dados_vendas()
    fig = px.bar(df, x="Mês", y="Vendas", color="Vendas", color_continuous_scale="Blues")
    fig.update_layout(**THEME, showlegend=False)
    return fig

@callback(Output("vendas-vs-meta", "figure"), Input("url", "pathname"))
def fig_vendas_meta(pathname):
    if pathname != "/vendas":
        return go.Figure()
    df = dados_vendas()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Vendas", x=df["Mês"], y=df["Vendas"], marker_color="#0078d4"))
    fig.add_trace(go.Line(name="Meta", x=df["Mês"], y=df["Meta"], line=dict(dash="dash", color="#107c10")))
    fig.update_layout(**THEME, barmode="group")
    return fig

@callback(Output("vendas-linha", "figure"), Input("url", "pathname"))
def fig_vendas_linha(pathname):
    if pathname != "/vendas":
        return go.Figure()
    df = serie_temporal()
    fig = go.Figure(go.Scatter(x=df["Data"], y=df["Valor"], mode="lines", line=dict(color="#0078d4", width=2)))
    fig.update_layout(**THEME)
    return fig

# --- Callbacks gráficos Operações ---
@callback(Output("ops-barras", "figure"), Input("url", "pathname"))
def fig_ops_barras(pathname):
    if pathname != "/operacoes":
        return go.Figure()
    df = dados_operacoes()
    fig = px.bar(df, x="Área", y="Atividades", color="Atividades", color_continuous_scale="Teal")
    fig.update_layout(**THEME, showlegend=False)
    return fig

@callback(Output("ops-gauge", "figure"), Input("url", "pathname"))
def fig_ops_gauge(pathname):
    if pathname != "/operacoes":
        return go.Figure()
    df = dados_operacoes()
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df["Concluído %"].mean(),
        number=dict(suffix="%"),
        gauge=dict(
            axis=dict(range=[0, 100]),
            bar=dict(color="#0078d4"),
            steps=[dict(range=[0, 70], color="#edebe9"), dict(range=[70, 90], color="#deecf1"), dict(range=[90, 100], color="#0078d4")],
            threshold=dict(line=dict(color="red", width=2), value=90),
        ),
    ))
    fig.update_layout(**THEME, height=280)
    return fig

@callback(Output("ops-pizza", "figure"), Input("url", "pathname"))
def fig_ops_pizza(pathname):
    if pathname != "/operacoes":
        return go.Figure()
    df = dados_operacoes()
    fig = px.pie(df, values="Atividades", names="Área", color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(**THEME, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    return fig

if __name__ == "__main__":
    app.run_server(host="127.0.0.1", port=8050, debug=False)
