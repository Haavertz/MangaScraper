# 🚀 Manga Update Checker (Automático)

Um bot que verifica sites de mangá a cada hora e detecta novos lançamentos usando GitHub Actions. Ideal para acompanhar suas séries favoritas!

## ⚡ Funcionalidades

- ✔️ Verifica múltiplos sites de mangá simultaneamente
- ✔️ Suporte a seletores CSS e XPath customizados
- ✔️ Salva o histórico de atualizações automaticamente
- ✔️ Notificações via Discord (opcional)
- ✔️ Execução agendada (cada 1 hora)

## 🛠️ Configuração

### Pré-requisitos

- Python 3.x
- Conta no GitHub

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/manga-checker.git
   cd manga-checker
2. **Instale os Dependências**
   ```bash
   pip install -r requirements.txt
3. **Configure os Sites**
   Edite o arquivo sites_config.json para adicionar os sites que deseja monitorar. Exemplo:
   ```
   {
    "sites": [
        {
            "name":"SiteExemplo",
            "url": "https://site.com/latest",
            "selector": ".classe-do-titulo",
            "type": "css"
        }
    ]
   }
   ```
## 👽 Como Usar

1. **Execute o Script**
    ```bash
    python scraper.py

2. **Resultado**
    Se houver novos capítulos, serão salvos em last_updates.json.
    Se não, você verá: Nenhuma atualização..

## 🤝 Contribuindo

### Contribuições são bem-vindas!

    1. Faça um fork do projeto.
    2. Crie uma branch (git checkout -b feature/nova-feature).
    3. Commit suas mudanças (git commit -m 'Adiciona suporte a X').
    4. Push para a branch (git push origin feature/nova-feature). 
    5. Abra um Pull Request.

## ⚠️ Aviso
    Respeite o robots.txt dos sites.
    Não faça requisições em excesso para evitar bloqueios.