import os
import requests
from bs4 import BeautifulSoup
import base64
import json

def download_manga(url_manga):
    nome_manga = url_manga.split('/')[-2]
    if not os.path.exists(nome_manga):
        os.makedirs(nome_manga)

    try:
        resposta = requests.get(url_manga)
        resposta.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url_manga}: {e}")
        return

    soup = BeautifulSoup(resposta.text, 'html.parser')
    lista_capitulos = soup.find_all('li', class_='wp-manga-chapter')

    for capitulo in lista_capitulos:
        titulo = capitulo.find('a').text.strip()
        url_capitulo = capitulo.find('a')['href']

        nome_capitulo = titulo.replace(' ', '_').replace('/', '_').replace(':', '_')
        caminho_capitulo = os.path.join(nome_manga, nome_capitulo)
        if not os.path.exists(caminho_capitulo):
            os.makedirs(caminho_capitulo)

        try:
            resposta_capitulo = requests.get(url_capitulo)
            resposta_capitulo.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url_capitulo}: {e}")
            continue

        soup_capitulo = BeautifulSoup(resposta_capitulo.text, 'html.parser')

        script_tag = soup_capitulo.find('script', text=lambda t: t and 'imageLinks' in t)
        if script_tag:
            image_links_json = json.loads(script_tag.string.split('imageLinks = ')[1].split(';')[0])
            for i, imageUrlEncoded in enumerate(image_links_json, start=1):
                url_imagem = base64.b64decode(imageUrlEncoded).decode('utf-8')

                try:
                    resposta_imagem = requests.get(url_imagem)
                    resposta_imagem.raise_for_status() 
                    caminho_imagem = os.path.join(caminho_capitulo, f'{i:03}.jpg')
                    with open(caminho_imagem, 'wb') as f:
                        f.write(resposta_imagem.content)
                    print(f"Baixando {caminho_imagem}")
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao baixar {url_imagem}: {e}")
        else:
            print("Não foi possível encontrar os links de imagens no capítulo.")

