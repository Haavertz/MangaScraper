import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://slimeread.com/"

def get_last_manga():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        possible_selectors = [
            ("h2", "grid-title"),
            ("div", "post-title"),
            ("div", "styletwo"),
            ("div", "utao"),
            ("span", "text-[15px] font-medium hover:text-themecolor hover:cursor-pointer"),
            ("a", "tw-wt dark:dark tw-vc tw-ke tw-qa tw-zp"),
            ("a", "manga-title"),
            ("h3", "chapter-title")
        ]

        current_date = datetime.now().strftime("%Y-%m-%d")
        current_day = datetime.now().strftime("%A")  
        with open("last_manga.txt", "a", encoding="utf-8") as f:
            for tag, class_name in possible_selectors:
                element = soup.find(tag, class_=class_name)
                if element:
                    last_manga = element.text.strip().splitlines()[0]
                    f.write(f"{current_date} ({current_day}) - {last_manga}\n")
                    return last_manga

        print("No title found. Check the 'site_content.html' file.")
        return None
    else:
        print(f"Failed to access the site: {response.status_code}")
        return None

if __name__ == "__main__":
    manga = get_last_manga()
    if manga:
        print(f"Last manga: {manga}")
