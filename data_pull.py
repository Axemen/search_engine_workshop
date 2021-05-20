import requests
from bs4 import BeautifulSoup
import re
from tqdm import trange

base_url = f"https://www.gutenberg.org"


for i in trange(1, 1000):
    try:
        html = requests.get(base_url + '/ebooks/' + str(i)).text
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find('a', text=re.compile("Plain Text UTF-8"))
        title = soup.find("h1", itemprop="name").text
        text = requests.get(base_url + a['href']).text
        if text: 
            with open(f"books/{title}.txt", 'w', encoding="utf-8") as f:
                f.write(text)
    except:
        pass
