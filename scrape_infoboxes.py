import requests
from bs4 import BeautifulSoup
import os

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
infobox_template_link_file = 'infobox_template_links.txt'

if not os.path.exists(infobox_template_link_file):
    for url in urls:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find and extract all the links in the page
            links = soup.find_all('a')

            # Print the links
            for link in links:
                href = link.get('href')
                if href and href.startswith("/wiki/") and 'Template:Infobox' in href:
                    # Filter links to Wikipedia articles by checking the URL
                    with open(infobox_template_link_file, 'a+') as f:
                        f.write(f'{href}\n')

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")


