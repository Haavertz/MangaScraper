import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import html
from datetime import datetime

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
        if ":" in container[1]:
            div_container = soup.select_one(f'.{container[1].replace(" ", ".").replace(":", "\\:")}')
        else:
            div_container = soup.select_one(f'.{container[1].replace(" ", ".")}')
        
        element_inside_container = div_container.find_all(element[0], class_=element[1])
        results = []
        for elem in element_inside_container:
            if link := elem.find('a'):
                title = link.get_text(strip=True)
                url = urljoin(site_config['url'], link.get('href'))
                results.append({"Title": title, "Url": url, "Time" : current_date})

        return results[:1]

    elif site_config['type'] == 'xpath':
        tree = html.fromstring(response.text)
        element = tree.xpath(site_config['selector'])[0]
    return element.text.strip() if element else None


def check_updates():
    try:
        with open('last_updates.json', 'r') as f:
            last_updates = json.load(f)
            for site in last_updates["sites"]:
                if isinstance(last_updates["sites"][site], dict):
                    last_updates["sites"][site] = [last_updates["sites"][site]]
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
        for site_name, entries in updates["sites"].items():
            last_updates["sites"][site_name] = entries
        
        with open('last_updates.json', 'w') as f:
            json.dump(last_updates, f, indent=3)
        return updates
    return None

if __name__ == "__main__":
    new_updates = check_updates()
    if new_updates:
        print("Updates found:")
        for site, data in new_updates["sites"].items():
            print(f"- {site}: {data[0]} ")
    else:
        print("No new updates.")