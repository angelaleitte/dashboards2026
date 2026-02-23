"""
Dashboard de exemplo - Plotly Dash
Para deploy no Dokploy em paineis.angelaleitte.com.br
"""
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random

# Dados de exemplo para os gráficos
def gerar_dados_exemplo():
    """Gera dados fictícios para demonstração."""
    random.seed(42)
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    vendas = [random.randint(80, 150) for _ in range(12)]
    visitas = [random.randint(200, 500) for _ in range(12)]
    return pd.DataFrame({
        'Mês': meses,
        'Vendas': vendas,
        'Visitas': visitas
    })

def gerar_serie_temporal():
    """Série temporal para gráfico de linha."""
    datas = pd.date_range(start='2024-01-01', periods=90, freq='D')
    valores = 100 + pd.Series(range(90)).apply(lambda x: random.gauss(0, 5)).cumsum()
    return pd.DataFrame({'Data': datas, 'Métrica': valores.clip(lower=50)})

# Inicialização do app Dash
app = dash.Dash(
    __name__,
    title="Painéis Angela Leitte",
    update_title="Carregando...",
    suppress_callback_exceptions=True
)

# Objeto server para Gunicorn
server = app.server

# Estilo e layout principal
app.layout = html.Div([
    html.Div([
        html.H1("📊 Painéis Angela Leitte", className="titulo"),
        html.P("Dashboard de exemplo — Plotly Dash no Dokploy", className="subtitulo"),
    ], className="header"),

    html.Div([
        html.Div([
            html.Div([
                html.H3("Vendas mensais", style={"marginBottom": "8px"}),
                dcc.Graph(id="grafico-vendas", config={"displayModeBar": True, "responsive": True}),
            ], className="card"),
        ], className="coluna"),
        html.Div([
            html.Div([
                html.H3("Visitas x Vendas", style={"marginBottom": "8px"}),
                dcc.Graph(id="grafico-dispersao", config={"displayModeBar": True, "responsive": True}),
            ], className="card"),
        ], className="coluna"),
    ], className="linha"),

    html.Div([
        html.Div([
            html.H3("Série temporal (exemplo)", style={"marginBottom": "8px"}),
            dcc.Graph(id="grafico-linha", config={"displayModeBar": True, "responsive": True}),
        ], className="card card-larga"),
    ], className="linha"),

    html.Footer("Dashboard de exemplo · Plotly Dash · paineis.angelaleitte.com.br", className="footer"),
], className="container")

# Callbacks
@app.callback(
    Output("grafico-vendas", "figure"),
    Input("grafico-vendas", "id")
)
def atualizar_vendas(_):
    df = gerar_dados_exemplo()
    fig = px.bar(df, x="Mês", y="Vendas", color="Vendas", color_continuous_scale="Blues")
    fig.update_layout(margin=dict(t=20, b=20, l=40, r=20), showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

@app.callback(
    Output("grafico-dispersao", "figure"),
    Input("grafico-dispersao", "id")
)
def atualizar_dispersao(_):
    df = gerar_dados_exemplo()
    fig = px.scatter(df, x="Visitas", y="Vendas", size="Vendas", color="Mês", hover_name="Mês")
    fig.update_layout(margin=dict(t=20, b=20, l=40, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

@app.callback(
    Output("grafico-linha", "figure"),
    Input("grafico-linha", "id")
)
def atualizar_linha(_):
    df = gerar_serie_temporal()
    fig = go.Figure(data=go.Scatter(x=df["Data"], y=df["Métrica"], mode="lines", line=dict(color="#2c3e50", width=2)))
    fig.update_layout(margin=dict(t=20, b=20, l=40, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
