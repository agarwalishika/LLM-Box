from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import os
import requests
import bz2

def load_from_wikidata(item):
    query = f"""
    SELECT ?pLabel ?prop ?val ?valLabel
    WHERE {{
    wd:{item} ?prop ?val .
    ?ps wikibase:directClaim ?prop .
    ?ps rdfs:label ?pLabel .
    ?val rdfs:label ?valLabel
    FILTER (LANG(?pLabel) = "en" && LANG(?valLabel) = "en"  && (?prop != wdt:P18) )
    }}
    """
    print(query)
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])

    return results_df

def process(df):
    df = df[["prop.value", "val.value","pLabel.value","valLabel.value"]]
    df = df.rename(columns={"prop.value":"pred","val.value":"obj","pLabel.value":"pLabel","valLabel.value":"vLabel"})
    df["trimmed_obj"] = df["obj"].apply(lambda x: x.split("/")[-1])
    return df


def load_df(item):
    file = f"Wikidata/{item}.pkl"
    file_raw = f"Wikidata/{item}_old.pkl"
    
    if os.path.exists(file):
        print("Loading stored dataframe")
        df = pd.read_pickle(file)
    elif os.path.exists(file_raw):
        print("Raw File found")
        df = pd.read_pickle(file_raw)
        df = process(df)
    else:
        print("Local Copy not found, loading from wikidata")
        df = load_from_wikidata(item)
        df.to_pickle(f"Wikidata/{item}_old.pkl")
        df = process(df)
    
    return df

def download_pagerank(file):
    if os.path.exists(file):
        print("PageRank file  exists")
        return
    # Specify the URL of the .bz2 file you want to download
    url = "https://danker.s3.amazonaws.com/2023-05-03.allwiki.links.rank.bz2"

    # Specify the local file name where you want to save the downloaded .bz2 file
    local_filename = "pagerank.bz2"

    # Specify the directory where you want to extract the contents
    extracted_dir = "pagerank.rank"

    # Download the .bz2 file
    response = requests.get(url)

    if response.status_code == 200:
        # Save the downloaded .bz2 file locally
        with open(local_filename, "wb") as file:
            file.write(response.content)

        # Extract the contents of the .bz2 file
        with bz2.BZ2File(local_filename, "rb") as source, open(extracted_dir, "wb") as target:
            for data in iter(lambda: source.read(100 * 1024), b''):
                target.write(data)

        print(f"File '{local_filename}' downloaded and extracted to '{extracted_dir}'.")
    else:
        print(f"Failed to download the file. HTTP Status Code: {response.status_code}")


os.makedirs("Wikidata",exist_ok=True)
os.makedirs("Infobox",exist_ok=True)

item = "Q42"
infobox_count = 30
pagerank_file = "pagerank.rank"
freq_file = "freq_file.csv"

freq = pd.read_csv(freq_file)
freq = freq.rename(columns={"predicate":"pred"})

download_pagerank(pagerank_file)
pagerank = pd.read_csv("pagerank.rank",delimiter='\t')
pagerank.columns = ["trimmed_obj","rank"]

df = load_df(item)

df = df.merge(freq, on="pred",how="left")
df = df.rename(columns={"count":"pred_count"})
min_pred_count = df['pred_count'].min()
max_pred_count = df['pred_count'].max()
df['norm_pred_count'] = (df['pred_count'] - min_pred_count) / (max_pred_count - min_pred_count)


df = df.merge(pagerank,on="trimmed_obj",how="left")
min_rank_value = df['rank'].min()
max_rank_value = df['rank'].max()
df['norm_obj_pagerank'] = (df['rank'] - min_rank_value) / (max_rank_value - min_rank_value)


df["rank_add"] = (df["norm_pred_count"] + df["norm_obj_pagerank"])/2
df["rank_mult"] = (df["norm_pred_count"]*df["norm_obj_pagerank"])

df.to_pickle(f"Wikidata/{item}.pkl")

if not os.path.exists(f"Infobox/{item}_rank_add.pkl") :
    df_rank_add = df.sort_values(by="rank_add",ascending=False).head(infobox_count)
    df_rank_add = df_rank_add[["pLabel","vLabel"]]
    print(df_rank_add)
    df_rank_add.to_pickle(f"Infobox/{item}_rank_add.pkl")

if not os.path.exists(f"Infobox/{item}_rank_mult.pkl") :
    df_rank_add = df.sort_values(by="rank_mult",ascending=False).head(infobox_count)
    df_rank_add = df_rank_add[["pLabel","vLabel"]]
    print(df_rank_add)
    df_rank_add.to_pickle(f"Infobox/{item}_rank_mult.pkl")