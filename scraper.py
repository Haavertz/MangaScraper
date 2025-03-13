import json
import requests
import discord
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

        container = site_config['container']
        element = site_config['selector']
        div_container = soup.select_one(f'.{container[1].replace(" ", ".").replace(":", "\\:")}')
        
        if not div_container:
            return None
        
        element_inside_container = div_container.find_all(element[0], class_=element[1])
        results = []
        for elem in element_inside_container:
            if link := elem.find('a'):
                title = link.get_text(strip=True)
                url = urljoin(site_config['url'], link.get('href'))
                results.append({"Title": title, "Url": url, "Time": current_date})
        return results[:1] if results else None

    elif site_config['type'] == 'xpath':
        tree = html.fromstring(response.text)
        elements = tree.xpath(site_config['selector'])
        return elements[0].text.strip() if elements else None

def check_updates():
    try:
        with open('last_updates.json', 'r') as f:
            last_updates = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        last_updates = {"sites": {}}

    sites = load_config()
    updates = {"sites": {}}

    for site in sites:
        site_name = site['name']
        latest_data = get_latest_manga(site)
        
        if latest_data:
            current_entry = latest_data[0]
            existing_entries = last_updates["sites"].get(site_name, [])
            
            if current_entry not in existing_entries:
                existing_entries.append(current_entry)
                updates["sites"][site_name] = existing_entries
                print(f"Novo capítulo adicionado para {site_name}!")

    if updates["sites"]:
        last_updates["sites"].update(updates["sites"])
        
        with open('last_updates.json', 'w') as f:
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
