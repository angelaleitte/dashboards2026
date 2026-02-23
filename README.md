# Dashboards Plotly/Dash — Dokploy (Hostinger)

Estrutura para rodar dashboards **Plotly Dash** no [Dokploy](https://dokploy.com) na VPS Hostinger, no subdomínio **paineis.angelaleitte.com.br**.

## Estrutura do projeto

```
dashDois/
├── app.py              # Aplicação Dash (dashboard de exemplo)
├── assets/
│   └── custom.css      # Estilos do dashboard
├── requirements.txt    # Dependências Python
├── Dockerfile         # Build da imagem
├── docker-compose.yml # Orquestração para Dokploy
├── .dockerignore
└── README.md
```

## Requisitos

- VPS com Docker e Dokploy instalado (Hostinger)
- Subdomínio **paineis.angelaleitte.com.br** apontando em DNS (registro **A**) para o IP da VPS

## Deploy no Dokploy

### 1. Repositório no Dokploy

- No Dokploy, crie um novo projeto (ex.: "Paineis").
- Adicione uma aplicação do tipo **Docker Compose**.
- Conecte o repositório Git (GitHub, GitLab, etc.) onde está este código **ou** use **Upload** (zip) com a pasta do projeto.

### 2. Build e deploy

- Dokploy usa o `docker-compose.yml` e o `Dockerfile` para build e subida.
- Em **Deploy**, faça o primeiro deploy. O build pode levar alguns minutos.

### 3. Configurar o domínio (paineis.angelaleitte.com.br)

- Abra a aplicação no Dokploy e vá na aba **Domains** (atalho `u`).
- Adicione um domínio:
  - **Host:** `paineis.angelaleitte.com.br`
  - **Container Port:** `8050` (porta do Dash)
  - Ative **HTTPS** e escolha **Let's Encrypt** para o certificado.
- Salve. O Traefik (proxy do Dokploy) passará a encaminhar o tráfego do subdomínio para o container na porta 8050.

### 4. DNS na Hostinger

No painel DNS do domínio **angelaleitte.com.br**:

- Tipo: **A**
- Nome: `paineis` (ou `paineis.angelaleitte.com.br`, conforme o painel)
- Valor: **IP da sua VPS**
- TTL: 3600 (ou padrão)

Aguarde a propagação (alguns minutos até 48h). Depois, **https://paineis.angelaleitte.com.br** deve abrir o dashboard.

### 5. Variáveis de ambiente (opcional)

Na aba **Environment** do Dokploy, você pode definir variáveis (ex.: chaves de API, debug). Elas são salvas em `.env` e carregadas pelo `docker-compose` com `env_file: - .env`.

Para usar no código, acesse via `os.environ.get("NOME_DA_VAR")` no `app.py`.

## Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python app.py
```

Acesse: **http://localhost:8050**

## Dashboard de exemplo

O `app.py` inclui um dashboard de exemplo com:

- **Gráfico de barras** — vendas mensais
- **Gráfico de dispersão** — visitas x vendas
- **Gráfico de linha** — série temporal

Você pode trocar os dados em `gerar_dados_exemplo()` e `gerar_serie_temporal()` por suas próprias fontes (CSV, API, banco).

## Produção

- A aplicação sobe com **Gunicorn** (1 worker, 4 threads), adequado para Dash.
- Para mais tráfego, aumente `--workers` no `Dockerfile` (cuidado: Dash mantém estado em memória por worker).
- Logs: aba **Logs** no Dokploy.
- Reinício automático: `restart: unless-stopped` no `docker-compose.yml`.

## Resumo rápido

| Item | Valor |
|------|--------|
| Subdomínio | paineis.angelaleitte.com.br |
| Porta no container | 8050 |
| Tipo de app no Dokploy | Docker Compose |
| Certificado HTTPS | Let's Encrypt (na aba Domains) |
