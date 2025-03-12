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
2. **Instale as Dependências**
   ```bash
   pip install -r requirements.txt

## 👽 Como Usar

1. **Configure os Sites**
   Edite o arquivo sites_config.json para adicionar os sites que deseja monitorar. Exemplo:
   ```
    {
    "sites": [
        {
            "name": "TestSiteExemplo",
            "url": "https://site.com",
            "container": ["container", "class"],
            "selector": ["element", "class"],
            "type": "css"
        }
    ]
    }
    ```
    Caso queira adicionar mais Sites, apenas siga essa mesma estrutura. Exemplo:
   ```
    {
    "sites": [
        {
            "name": "TestSiteExemplo",
            "url": "https://site.com",
            "container": ["container", "class"],
            "selector": ["element", "class"],
            "type": "css"
        },
        {
            "name": "TestSiteExemplo2",
            "url": "https://site.com",
            "container": ["container", "class"],
            "selector": ["element", "class"],
            "type": "css"
        }
    ]
    }
    ```

2. **Como Modificar**

    name -> Coloque o Nome que sera salvo no arquivo last_updates
    url -> Voce ira colocar a URL do site que deseja monitorar
    *container* -> index 0 voce ira colocar o tipo do ELEMENTO (divs, main, section, etc...) que ficam os capitulos ATUALIZADOS! 
    no index 1 voce ira colocar a CLASSE que esse ELEMENTO tem.
    *selector* -> index 0 voce ira colocar o ELEMENTO anterior que estive o LINK para a obra, no index 1 voce ira colocar a CLASSE 
    que esse ELEMENTO tem.

    Container:
    ```
        <div class"grid grid-rows-1 grid-cols-1 sm:grid-cols-2">
            <div class="w-full p-1 pt-1 pb-3 border-b-[1px] border-b-[#312f40]">
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

    Selector:
    ```
        <span class="font-medium">
            <a href="/series/return-of-the-disaster-class-hero-429615ff">Return of the Disaster-Class H...</a>
        </span>
    ```

    Exemplo - 01:
    ```

    {
      "name": "Asura",
      "url": "https://asuracomic.net",
      "container": ["div", "grid grid-rows-1 grid-cols-1 sm:grid-cols-2"], -> nao deixe espaco no final e nem antes!
      "selector": ["span", "font-medium"], -> nao deixe espaco no final e nem antes!
      "type": "css"
    }

    ```

3. **Resultado**
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
    O Projeto esta se iniciando tem muito o que melhorar.