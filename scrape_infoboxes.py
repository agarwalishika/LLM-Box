import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from config import *

def get_soup(link_url):
    response = requests.get(link_url)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        0/0


# Define the URL of the Wikipedia page you want to scrape
urls = ['https://en.wikipedia.org/wiki/Category:Infobox_templates', 
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=bird%2Ftestcases%0AInfobox+bird%2Ftestcases#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=comics+nationality%0AInfobox+comics+nationality#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=European+Games+sport%0AInfobox+European+Games+sport#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=guitar+pickup%0AInfobox+guitar+pickup#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=Laser+module%0AInfobox+Laser+module#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=national+baseball+team%0AInfobox+national+baseball+team#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=Philippine+Congress%0AInfobox+Philippine+Congress#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=Russian+inhabited+locality%0AInfobox+Russian+inhabited+locality#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=tea%0AInfobox+tea#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:Infobox_templates&pagefrom=windstorm+season%0AInfobox+windstorm+season#mw-pages']


if not os.path.exists(infobox_template_link_file):
    for url in urls:
        # Send an HTTP GET request to the URL
        soup = get_soup(url)

        # Find and extract all the links in the page
        links = soup.find_all('a')

        # Print the links
        for link in links:
            href = link.get('href')
            if href and href.startswith("/wiki/") and 'Template:Infobox' in href:
                # Filter links to Wikipedia articles by checking the URL
                with open(infobox_template_link_file, 'a+') as f:
                    f.write(f'{href}\n')
    print('scraped for infobox template links')

if not os.path.exists(infobox_templates_file):
    filter_text = "{{Infobox"
    
    def get_fields(temp):
        try:
            x = temp.index(filter_text)
            infobox_raw = temp[x: x+temp[x:].index("}}")]
            infobox_raw = infobox_raw[infobox_raw.index("|"):]
            infobox_raw = infobox_raw.split("|")
            fields = []
            for sep in infobox_raw:
                if len(sep):
                    sep = sep.strip().split(' ')[0]
                    fields.append(sep)
            return fields
        except ValueError:
            return -1
        except:
            return x
        
    links = None
    with open(infobox_template_link_file, 'r') as f:
        links = f.readlines()

    for link in tqdm(links):
        try:
            soup = get_soup(f'{prefix}{link[:-1]}')
            temp = soup.get_text()
            fields = get_fields(temp)
            if type(fields) is int and fields < 0:
                continue # this wiki does not have an infobox template

            pointer = 0

            while(type(fields) is int):
                pointer += fields + len(filter_text)
                fields = get_fields(temp[pointer:])
            
            with open(infobox_templates_file, 'a+') as w:
                w.write(f'{link[15:].strip()} {" ".join(fields)}\n')
        except:
            with open('failed_infobox_templates.txt', "a+") as f:
                f.write(f'didnt work for {link}\n')
    print('scraped the fields of infobox templates')
else:
    print('try again')
