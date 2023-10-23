"""
Steps: 
1. split infobox_template_with_fields.txt into individual files
2. use langchain and chroma to create a vectordb from the directory fo files from (1) and persist it to disk
3. get article as a supplement to prompt
4. chunk the article and provide the prompt to retrieve the infobox template
5. use the infobox template retrieved from the vector database as a supplement to the prompt
6. provide the prompt to populate the infobox fields with text from the article. 
"""
import re
import os
import chromadb
from tqdm import tqdm
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document



## Step 1: Split infobox scrape file into individual files
# with open("./infobox_template_with_fields.txt", 'r') as infoboxes:
#     Lines = infoboxes.readlines()
 
#     count = 0
#     # Strips the newline character
#     for line in Lines:
#         count += 1
#         parts = line.split()
#         fname = parts[0]
#         fname = re.sub("[^a-zA-Z0-9_]", '', fname)

#         with open("./QueryPipeline/infoboxes/{0}.txt".format(fname), "w") as newFile:
#             newFile.writelines([line])

## Step 2: create and persist chroma vector db



# client = chromadb.PersistentClient(path="./QueryPipeline/")
# # client.delete_collection(name="infoboxes")

# collection = client.create_collection(name="infoboxes")

# with open("./infobox_template_with_fields.txt", 'r') as infoboxes:
#     Lines = infoboxes.readlines()
#     fnames = list(map(lambda line: re.sub("[^a-zA-Z0-9_]", '', line.split()[0]),Lines))
#     collection.add(
#         documents=Lines,
#         metadatas=[{"source":fname} for fname in fnames],
#         ids=fnames
#     )

# langchain_chroma = Chroma(
#     client=client,
#     collection_name="infoboxes",
#     embedding_function=OpenAIEmbeddings(openai_api_key="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"),
# )



## Step 3: Use an article as a query supplement

client = chromadb.PersistentClient(path="./QueryPipeline/")

collection = client.get_collection(name="infoboxes")

langchain_chroma = Chroma(
    client=client,
    collection_name="infoboxes",
    embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
)

# print("There are", langchain_chroma._collection.count(), "in the collection")

query = "The red-winged blackbird (Agelaius phoeniceus) is a passerine bird of the family Icteridae found in most of North America and much of Central America. It breeds from Alaska and Newfoundland south to Florida, the Gulf of Mexico, Mexico, and Guatemala, with isolated populations in western El Salvador, northwestern Honduras, and northwestern Costa Rica. It may winter as far north as Pennsylvania and British Columbia, but northern populations are generally migratory, moving south to Mexico and the Southern United States. Claims have been made that it is the most abundant living land bird in North America, as bird-counting censuses of wintering red-winged blackbirds sometimes show that loose flocks can number in excess of a million birds per flock and the full number of breeding pairs across North and Central America may exceed 250 million in peak years. It also ranks among the best-studied wild bird species in the world.[2][3][4][5][6] The red-winged blackbird is sexually dimorphic; the male is all black with a red shoulder and yellow wing bar, while the female is a nondescript dark brown. Seeds and insects make up the bulk of the red-winged blackbird's diet."
docs = langchain_chroma.similarity_search(query)
for el in docs:
    print(el)
    print("==========================")
