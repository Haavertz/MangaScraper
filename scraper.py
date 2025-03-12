import requests
from bs4 import BeautifulSoup

URL = "https://seitacelestial.com/"

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
            ("a", "manga-title"),
            ("h3", "chapter-title")
        ]

        for tag, class_name in possible_selectors:
            element = soup.find(tag, class_=class_name)
            if element:
                last_manga = element.text.strip().splitlines()[0]
                
                with open("last_manga.txt", "w", encoding="utf-8") as f:
                    f.write(last_manga)
                return last_manga

        with open("site_content.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        
        print("No title found. Check the 'site_content.html' file.")
        return None
    else:
        print(f"Failed to access the site: {response.status_code}")
        return None

if __name__ == "__main__":
    manga = get_last_manga()
    if manga:
        print(f"Last manga: {manga}")
