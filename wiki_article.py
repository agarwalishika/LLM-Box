import wikipediaapi
import re

# Define the article title you want to extract the infobox from
article_title = "Python (programming language)"

# Create a Wikipedia API client
wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent="your_app_name/1.0")

# Fetch the article content
page = wiki_wiki.page(article_title)

print(page.text)

# Extract the infobox using regular expressions
# infobox = re.search(r'{{Infobox.*?}}', page.text, re.DOTALL)

# if infobox:
#     infobox_text = infobox.group()
#     print(infobox_text)
# else:
#     print("Infobox not found in the article.")