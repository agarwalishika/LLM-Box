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
import numpy as np
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
# client.delete_collection(name="infoboxes")

# collection = client.create_collection(name="infoboxes", metadata={"hnsw:space": "l2"})

# with open("./infobox_template_with_fields.txt", 'r') as infoboxes:
#     Lines = infoboxes.readlines()
#     fnames = list(map(lambda line: re.sub("[^a-zA-Z0-9_]", '', line.split()[0]),Lines))
#     Lines = list(map(lambda line: (line.split()[0].replace("_", " ") + " ")*5 + " "+ line,Lines))
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

# query = "The red-winged blackbird (Agelaius phoeniceus) is a passerine bird of the family Icteridae found in most of North America and much of Central America. It breeds from Alaska and Newfoundland south to Florida, the Gulf of Mexico, Mexico, and Guatemala, with isolated populations in western El Salvador, northwestern Honduras, and northwestern Costa Rica. It may winter as far north as Pennsylvania and British Columbia, but northern populations are generally migratory, moving south to Mexico and the Southern United States. Claims have been made that it is the most abundant living land bird in North America, as bird-counting censuses of wintering red-winged blackbirds sometimes show that loose flocks can number in excess of a million birds per flock and the full number of breeding pairs across North and Central America may exceed 250 million in peak years. It also ranks among the best-studied wild bird species in the world.[2][3][4][5][6] The red-winged blackbird is sexually dimorphic; the male is all black with a red shoulder and yellow wing bar, while the female is a nondescript dark brown. Seeds and insects make up the bulk of the red-winged blackbird's diet."
# query = """Ramesses II[a] (/ˈræməsiːz, ˈræmsiːz, ˈræmziːz/; Ancient Egyptian: rꜥ-ms-sw, Rīꜥa-masē-sə,[b] Semitic pronunciation: [ɾiːʕamaˈseːsə]; c. 1303 BC – 1213 BC),[7] commonly known as Ramesses the Great, was an Egyptian pharaoh. He was the third ruler of the Nineteenth Dynasty. Along with Thutmose III of the Eighteenth Dynasty, he is often regarded as the greatest, most celebrated, and most powerful pharaoh of the New Kingdom, which itself was the most powerful period of ancient Egypt.[8] He is also widely considered one of ancient Egypt's most successful warrior pharaohs, conducting no fewer than 15 military campaigns, all resulting in victories, excluding the Battle of Kadesh, generally considered a stalemate.[9]

# In ancient Greek sources, he is called Ozymandias,[c][10] derived from the first part of his Egyptian-language regnal name: Usermaatre Setepenre.[d][11] Ramesses was also referred to as the "Great Ancestor" by successor pharaohs and the Egyptian people.

# For the early part of his reign, he focused on building cities, temples, and monuments. After establishing the city of Pi-Ramesses in the Nile Delta, he designated it as Egypt's new capital and used it as the main staging point for his campaigns in Syria. Ramesses led several military expeditions into the Levant, where he reasserted Egyptian control over Canaan and Phoenicia; he also led a number of expeditions into Nubia, all commemorated in inscriptions at Beit el-Wali and Gerf Hussein. He celebrated an unprecedented thirteen or fourteen Sed festivals—more than any other pharaoh.[12]

# Estimates of his age at death vary, though 90 or 91 is considered to be the most likely figure.[13][14] Upon his death, he was buried in a tomb (KV7) in the Valley of the Kings;[15] his body was later moved to the Royal Cache, where it was discovered by archaeologists in 1881. Ramesses' mummy is now on display at the National Museum of Egyptian Civilization, located in the city of Cairo.[16]"""

# query = """
# Star Wars comics have been produced by various comic book publishers since the debut of the 1977 film Star Wars.[a] Marvel Comics launched its original series in 1977, beginning with a six-issue comic adaptation of the film and running for 107 issues, including an adaptation of The Empire Strikes Back. Marvel also released an adaptation of Return of the Jedi and spin-offs based on Droids and Ewoks. A self-titled comic strip ran in American newspapers between 1979 and 1984. Blackthorne Publishing released a three-issue run of 3-D comics from 1987 to 1988.

# Dark Horse Comics published the limited series Dark Empire in 1991, and ultimately produced over 100 Star Wars titles, including Tales of the Jedi (1993–1998), X-wing: Rogue Squadron (1995–1998), Republic (1998–2006), Tales (1999–2005), Empire (2002–2006), Knights of the Old Republic (2006–2010), and Legacy (2006–2010), as well as manga adaptations of the original film trilogy and the 1999 prequel The Phantom Menace.

# The Walt Disney Company acquired Marvel in 2009 and Lucasfilm in 2012, and the Star Wars comics license returned to Marvel in 2015. Several new series were launched, including Star Wars, Star Wars: Darth Vader, and Doctor Aphra. In 2017, IDW Publishing launched the anthology series Star Wars Adventures. In 2022, Dark Horse resumed publishing new Star Wars comics and graphic novels.
# """

query = """
Sung Ji-hyun (Korean: 성지현; Hanja: 成池鉉; born 29 July 1991) is a South Korean badminton player from Seoul. She is an Asian Championship gold medalist, a two-time Summer Universiade gold medalist, and a World Championship bronze medalist. She was also part of South Korean teams that won the 2010 Uber Cup, 2017 Sudirman Cup, as well the team event at the 2013 and 2015 Summer Universiade.[1][2] She competed at the 2010, 2014 and 2018 Asian Games, and at the 2012 and 2016 Summer Olympics.[3] Sung is married to compatriot men's singles player, Son Wan-ho.[4] badminton_player badminton_player badminton_player badminton_player badminton_player badminton_player badminton_player badminton_player
"""
docs = langchain_chroma.similarity_search(query)
for el in docs:
    print(el)
    print("==========================")

## Step 4
# model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# #Our sentences we like to encode
# sentences = ['Infobox_bird collapsible state pop1 data1 unit lengthm lengthf culmen wing tail tarsus wingspan',
#              'Infobox_Isle_of_Man_TT_races year image alt caption date location course race1 race1_pole race1_pole_speed race1_fast race1_fast_speed race1_1st race1_2nd race1_3rd race2 race2_pole race2_pole_speed race2_fast race2_fast_speed race2_1st race2_2nd race2_3rd race3 race3_pole race3_pole_speed race3_fast race3_fast_speed race3_1st race3_2nd race3_3rd race4 race4_pole race4_pole_speed race4_fast race4_fast_speed race4_1st race4_2nd race4_3rd race5 race5_pole race5_pole_speed race5_fast race5_fast_speed race5_1st race5_2nd race5_3rd race6 race6_pole race6_pole_speed race6_fast race6_fast_speed race6_1st race6_2nd race6_3rd race7 race7_pole race7_pole_speed race7_fast race7_fast_speed race7_1st race7_2nd race7_3rd race8 race8_pole race8_pole_speed race8_fast race8_fast_speed race8_1st race8_2nd race8_3rd']

# query = 'The red-winged blackbird (Agelaius phoeniceus) is a passerine bird of the family Icteridae found in most of North America and much of Central America. It breeds from Alaska and Newfoundland south to Florida, the Gulf of Mexico, Mexico, and Guatemala, with isolated populations in western El Salvador, northwestern Honduras, and northwestern Costa Rica. It may winter as far north as Pennsylvania and British Columbia, but northern populations are generally migratory, moving south to Mexico and the Southern United States. Claims have been made that it is the most abundant living land bird in North America, as bird-counting censuses of wintering red-winged blackbirds sometimes show that loose flocks can number in excess of a million birds per flock and the full number of breeding pairs across North and Central America may exceed 250 million in peak years. It also ranks among the best-studied wild bird species in the world.[2][3][4][5][6] The red-winged blackbird is sexually dimorphic; the male is all black with a red shoulder and yellow wing bar, while the female is a nondescript dark brown. Seeds and insects make up the bulk of the red-winged blackbird\'s diet.'
# #Sentences are encoded by calling model.encode()
# embeddings = np.array(model.embed_documents(sentences))
# q_embeddings = np.array(model.embed_query(query))

# from numpy import dot
# from numpy.linalg import norm


# #Print the embeddings
# for sentence, embedding in zip(sentences, embeddings):
#     print("Sentence:", sentence)
#     cos_sim = dot(embedding,q_embeddings)/(norm(embedding)*norm(q_embeddings))
#     print("Difference:", cos_sim)
#     print()


