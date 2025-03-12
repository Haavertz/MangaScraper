# 🚀 MangaScraper (Automático)

Um bot que verifica sites de mangá a cada hora e detecta novos lançamentos usando GitHub Actions. Ideal para acompanhar suas séries favoritas!

**Lembrando que este software serve apenas para VERIFICAR se há capítulo novo. Caso queira ler, será necessário acessar o site oficial da Scan.**


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
   git clone https://github.com/Haavertz/MangaScraper.git
   cd MangaScraper
2. **Instale as Dependências**
   ```bash
   pip install -r requirements.txt

## 👽 Como Usar

1. ### Configure os Sites
   Edite o arquivo sites_config.json para adicionar os sites que deseja monitorar. Exemplo:
   ```
    {
    "sites": [
        {
        "name": "NomeExemplo",
        "url": "https://site.com",
        "container": ["elemento_container", "classe_container"],
        "selector": ["elemento_link", "classe_link"],
        "type": "css"
        }
    ]
    }
    ```
    Caso queira adicionar mais Sites, apenas siga essa mesma estrutura. Exemplo:
   ```
    {
        "sites": [
            { ... }, // Configuração Site 1
            { ... }  // Configuração Site 2
        ]
    }
    ```

2. ### Configurações do Monitoramento

    Este arquivo descreve as configurações que devem ser usadas para monitorar atualizações de sites.

    ### Parâmetros

    | Parâmetro   | Descrição                                                           | Exemplo                                                        |
    |--------------|---------------------------------------------------------------------|----------------------------------------------------------------|
    | `name`       | Nome identificador (será salvo em `last_updates.json`)              | `"Asura"`                                                      |
    | `url`        | URL completa do site a ser monitorado                               | `"https://asuracomic.net"`                                     |
    | `container`  | Elemento HTML e classe que envolve a lista de atualizações          | `["div", "grid grid-rows-1..."]`                               |
    | `selector`   | Elemento HTML e classe que contém o link do capítulo dentro do container | `["span", "font-medium"]`                                      |
    | `type`       | Tipo de seleção (atualmente suporta `"css"` para seletores de classe/elemento) | `"css"`                                                        |

    ### Exemplo de Configuração

    ```json
    {
    "name": "Asura",
    "url": "https://asuracomic.net",
    "container": ["div", "grid grid-rows-1 grid-cols-1 sm:grid-cols-2"],
    "selector": ["span", "font-medium"],
    "type": "css"
    }

    ```
    **Container:**
    ```
        <div class"grid grid-rows-1 grid-cols-1 sm:grid-cols-2">
            <div class="w-full p-1 pt-1 pb-3">
                <div class="grid grid-rows-1 grid-cols-12 m-2">
                    <div class="class="col-span-9 space-y-1.5 overflow-hidden">
                        <span class="font-medium">
                            <a href="/series/return-of-the-disaster-class-hero-429615ff">Return of the Disaster-Class H...</a>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    ```

    **Selector:**
    
    ```
        <span class="font-medium">
            <a href="/series/return-of-the-disaster-class-hero-429615ff">Return of the Disaster-Class H...</a>
        </span>
    ```


## 🤝 Contribuindo

### Contribuições são bem-vindas!

1. Faça um fork do projeto.
2. Crie uma branch (git checkout -b feature/nova-feature).
3. Commit suas mudanças (git commit -m 'Adiciona suporte a X').
4. Push para a branch (git push origin feature/nova-feature). 
5. Abra um Pull Request.

## ⚠️ Aviso
1. Respeite o robots.txt dos sites.
2. O projeto está em estágio inicial e muitas mudanças ainda ocorrerão.
