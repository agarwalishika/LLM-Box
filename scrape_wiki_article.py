from bs4 import BeautifulSoup
import requests
 
page = requests.get("https://en.wikipedia.org/wiki/Barack_Obama")

# scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')
 
infobox = soup.find("table", {"class": "infobox"})

if infobox:

    infobox_data = {}
    rows = infobox.find_all("tr")
    for row in rows:
        header = row.find("th")
        data = row.find("td")
        if header and data:
            key = header.get_text(strip=True)
            value = data.get_text(strip=True)
            infobox_data[key] = value

        elif header:
            key = header.get_text().strip().replace("\n", " ")
            infobox_data[key] = key
        
        elif data:
            key = data.get_text().strip().replace("\n", " ")
            infobox_data[key] = key

    if "" in infobox_data:
        del infobox_data[""]
    if " " in infobox_data:
        del infobox_data[" "]
    for key, value in infobox_data.items():
        print(f"{key}: {value}")
else:
    print("Infobox not found in the article.")

# page = requests.get("https://en.wikipedia.org/wiki/Python_(programming_language)")
 
# page = requests.get("https://en.wikipedia.org/w/index.php?title=Barack_Obama&action=edit")