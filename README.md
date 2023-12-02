## LLM-Box

### Group 2

## Run the repository
This repository contains all scripts required for the project LLM-Box. Below we describe how to run the different components:

### Data Collection
`data_collection` folder contains the scripts for collecting Wikipedia articles and infoboxes.

- Run `python3 scrape_wiki_article.py` to collect Wikipedia articles. Replace the first link for the article you wish to scrape.
- Run `python3 scrape_infoboxes.py` to collect infoboxes and pages for different templates.

### Data 

`articles` folder contains the Wikipedia articles and the generated infoboxes for our methodology.

### Vector database

- Run `python3 parse_articles_to_vdb.py` to convert articles to the vector database format. 
- This should generate a vector database in the `./chroma_db` directory.

### Stitch it together
- `run.ipynb` is the Jupyter notebook for executing the main pipeline once data collection is done and vector DB is set up.
- You can also run `inference_demo.ipynb` to check if all steps till now work fine.

### Evaluation

- The notebook `calculate_similarity.ipynb` computes the ROUGE, BLEU, ad word overlap statistics. 

- Run `python3 manual_eval.py` to do a manual evaluation of the infoboxes - samples randomly from generated or ground truth infoboxes, displays them in the browser, and requires you to to answer the manual eval questions.


### Baselines

`Baselines`: Contains baseline models for initial benchmarking.

Run `python3 generate_infobox.py` to generate infoboxes from the baseline methods. `Infobox` and `Wikidata` folders are tertiary folders required for the various baselines.