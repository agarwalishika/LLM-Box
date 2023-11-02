import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
from scipy import spatial  # for calculating vector similarities for search
from bs4 import BeautifulSoup
import requests
import re
import os
import chromadb
import numpy as np
from tqdm import tqdm
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

from config import *
openai.api_key = OPENAI_API_KEY

def get_soup(link_url):
    response = requests.get(link_url)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        0/0

def get_infobox_fields_as_metadata(link):
    filter_text = "{{Infobox"
    try:
        soup = get_soup(link)
        temp = soup.get_text()
        fields = get_fields(temp)
        pointer = 0

        while(type(fields) is int):
            pointer += fields + len(filter_text)
            fields = get_fields(temp[pointer:])
        parts = link.split(':')
        return f'{parts[-1]} {" ".join(fields)}'
    except:
        with open('failed_infobox_templates.txt', "a+") as f:
            f.write(f'didnt work for {link}\n')

def get_fields(temp):
    filter_text = "{{Infobox"
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

def scrape_article_from_link(link):
    import wikipedia

    # Set the language for the Wikipedia you want to access (e.g., 'en' for English)
    wikipedia.set_lang("en")

    # Replace 'Your_Article_Title' with the title of the Wikipedia article you want to access
    article_title = link.split('/')[-1]

    try:
        # Fetch the page for the given article title
        page = wikipedia.page(article_title)

        # Print the title of the article
        return f"Title: {page.title} \n Content: {page.content}"
    except:
        return -1
    
def generate_documents_for_article(text, metadata):
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 250,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
)

    texts = text_splitter.create_documents([text])
    source_chunks = []
    for chunk in texts:
        source_chunks.append(Document(page_content=chunk.page_content, metadata=metadata))
    return source_chunks

def assign_metadata_to_source_docs(template_links):
    docs = []
    
    for l in tqdm(template_links):
        print("")
        print("Getting infobox and articles for:", l)
        
        # Extract the infobox template as metadata for the vdb
        metadata = get_infobox_fields_as_metadata(l)

        infobox_template = l.split("Infobox_")[-1].split("_")
        og_link = "https://en.wikipedia.org/wiki/Special:WhatLinksHere?target=Template%3AInfobox+"
        link = og_link
        for entity in infobox_template:
                link += entity + "+"
        link += "&namespace="
        # link = 'https://en.wikipedia.org/wiki/Special:WhatLinksHere?target=Template%3AInfobox+comics+character&namespace='
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html.parser')

        links = []
        start = False
        for s in soup.find_all('a'):
            temp = s.get('href')
            try:
                if start and 'limit=50&dir=next' in temp:
                    break
                elif start:
                    links.append(temp)
                elif '&limit=500' in temp:
                    start = True
            except:
                    print("error: ", temp)              
        
        i = 0
        for link in links:
            if "/wiki" in link.lower():
                i += 1
                art = scrape_article_from_link(link)
                if art == -1:
                        continue
                docs += generate_documents_for_article(text=art, metadata={"schema":metadata})
            if i >= 5:
                break
    return docs

def batch_documents(docs, chunk_size):
    for i in range(0, len(docs), chunk_size):
        if i + chunk_size < len(docs):
            yield docs[i:i+chunk_size]
        else: 
            yield docs[i:]

if __name__=="__main__":

    template_links = [
            "https://en.wikipedia.org/wiki/Template:Infobox_character", 
            "https://en.wikipedia.org/wiki/Template:Infobox_comics_character",
            "https://en.wikipedia.org/wiki/Template:Infobox_mythical_creature",
            "https://en.wikipedia.org/wiki/Template:Infobox_award",
            "https://en.wikipedia.org/wiki/Template:Infobox_film",
            "https://en.wikipedia.org/wiki/Template:Infobox_book",
            "https://en.wikipedia.org/wiki/Template:Infobox_short_story",
            "https://en.wikipedia.org/wiki/Template:Infobox_flag",
            "https://en.wikipedia.org/wiki/Template:Infobox_Doctor_Who_episode",
            "https://en.wikipedia.org/wiki/Template:Infobox_medical_condition",
            "https://en.wikipedia.org/wiki/Template:Infobox_drug",
            "https://en.wikipedia.org/wiki/Template:Infobox_medical_intervention",
            "https://en.wikipedia.org/wiki/Template:Infobox_civil_conflict",
            "https://en.wikipedia.org/wiki/Template:Infobox_civilian_attack",
            "https://en.wikipedia.org/wiki/Template:Infobox_knot",
            "https://en.wikipedia.org/wiki/Template:Infobox_pharaoh",
            "https://en.wikipedia.org/wiki/Template:Infobox_noble",
            "https://en.wikipedia.org/wiki/Template:Infobox_Le_Mans_driver",
            "https://en.wikipedia.org/wiki/Template:Infobox_Motocross_rider",
            "https://en.wikipedia.org/wiki/Template:Infobox_scientist"
    ]

    docs = assign_metadata_to_source_docs(template_links)

    # print(docs)
    for batch in tqdm(batch_documents(docs, 1000)):
        db2 = Chroma.from_documents(batch,  
                                SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"), 
                                persist_directory="./chroma_db")
        db2.persist()

    print("Successfully created vector db!")
