import json
import requests
from bs4 import BeautifulSoup
from lxml import html


def load_config():
    with open('sites_config.json') as f:
        return json.load(f)['sites']


def get_latest_manga(site_config):
    response = requests.get(site_config['url'])

    if site_config['type'] == 'css':
        soup = BeautifulSoup(response.text, 'html.parser')

        container = site_config['container']
        element = site_config['selector']
        div_container = soup.select_one(f'.{container[1].replace(" ", ".")}')
        
        element_inside_container = div_container.find_all(element[0], class_=element[1])

        name = ""

        for tag in element_inside_container:
            link_tag = tag.find('a')
            
            if link_tag:
                name += link_tag.get_text() + "\n"

        return name.splitlines()[0]

    # elif site_config['type'] == 'xpath':
    #     tree = html.fromstring(response.text)
    #     element = tree.xpath(site_config['selector'])[0]
    # return element.text.strip() if element else None


def check_updates():

    try:
        with open('last_updates.json', 'r') as f:
            last_updates = json.load(f)
    except FileNotFoundError:
        last_updates = {}

    sites = load_config()

    updates = {}
    for site in sites:
        latest = get_latest_manga(site)
        if latest and latest != last_updates.get(site['name']):
            updates[site['name']] = latest

    if updates:
        with open('last_updates.json', 'w') as f:
            json.dump({**last_updates, **updates}, f)
        return updates
    return None


if __name__ == "__main__":
    new_updates = check_updates()
    if new_updates:
        print(f"New Chapter: {new_updates}")
    else:
        print("No Update.")