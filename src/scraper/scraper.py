import json
import requests
import discord
import unicodedata
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import html
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()  
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID")) 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def load_config():
    with open('sites_config.json') as f:
        return json.load(f)['sites']

def get_latest_manga(site_config):
    response = requests.get(site_config['url'])
    if site_config['type'] == 'css':
        soup = BeautifulSoup(response.text, 'html.parser')
        current_date = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H:%M:%S")

        container = site_config['container']
        element = site_config['selector']

        container_tag = container[0]
        container_class = container[1].replace(' ', '.').replace(':', '\\:')
        container_selector = f'{container_tag}.{container_class}'
        div_container = soup.select_one(container_selector)
        
        if not div_container:
            return None
        
        element_inside_container = []
        
        if len(element) == 2:
            elements = div_container.find_all(element[0], class_=element[1])
            element_inside_container = elements

        elif len(element) == 3:
            parent_elements = div_container.find_all(element[0], class_=element[1])
            for parent in parent_elements:
                children = parent.find_all(element[2])
                element_inside_container.extend(children)
        
        results = []
        for elem in element_inside_container:
            link = elem if elem.name == 'a' else elem.find('a')
            if link:
                title = unicodedata.normalize("NFKD", link.get_text(strip=True)).encode("ASCII", "ignore").decode("ASCII").title()
                url = urljoin(site_config['url'], link.get('href'))
                results.append({"Title": title, "Url": url, "Time": current_date, "Hours": time_now})


        idx = verify_manga_read(results, site_config)
        return results[0:idx:1] if results else None

    elif site_config['type'] == 'xpath':
        tree = html.fromstring(response.text)
        elements = tree.xpath(site_config['selector'])
        return elements[0].text.strip() if elements else None
    

def verify_manga_read(manga, site_name):

    with open('./src/json/last_updates.json', 'r') as f:
        last = json.load(f)

    passed_manga = None
    manga_site = last['sites'][site_name['name']][-1]['Title']
    for idx, i in enumerate(manga):
        title1 = unicodedata.normalize("NFKD", str(i['Title'])).encode("ASCII", "ignore").decode("ASCII").lower()
        title2 = unicodedata.normalize("NFKD", str(manga_site)).encode("ASCII", "ignore").decode("ASCII").lower()
        
        if title1 == title2:
            print(idx, i['Title'])
            passed_manga = idx
    
    return passed_manga

def check_updates():
    try:
        with open('./src/json/last_updates.json', 'r') as f:
            last_updates = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        last_updates = {"sites": {}}

    sites = load_config()
    updates = {"sites": {}}

    for site in sites:
        site_name = site['name']
        latest_data = get_latest_manga(site)

        if latest_data:
            existing_entries = last_updates["sites"].get(site_name, [])
            
            reversed_latest_data = list(reversed(latest_data))
            
            new_entries = [entry for entry in reversed_latest_data if entry not in existing_entries]

            if new_entries:
                existing_entries.extend(new_entries)
                updates["sites"][site_name] = existing_entries
                print(f"✅ Novos capítulos adicionados para {site_name}!")

    if updates["sites"]:
        last_updates["sites"].update(updates["sites"])
        
        with open('./src/json/last_updates.json', 'w') as f:
            json.dump(last_updates, f, indent=3)

        return updates

    return None


@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        updates = check_updates()
        if updates:
            for site_name, entries in updates["sites"].items():
                for entry in entries[-1:]:  
                    message = f"📢 Novo capítulo disponível em {site_name}!\n📖 {entry['Title']}\n 🔗 {entry['Url']}"
                    await channel.send(message)
    else:
        print("❌ Não foi possível encontrar o canal.")

bot.run(DISCORD_TOKEN)
