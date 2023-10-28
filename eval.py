import wikipediaapi
import re
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from datasets import load_dataset
import wikipediaapi
import csv

model_name= "deepset/roberta-base-squad2"
dataset   = load_dataset("wiki_qa")
questions = dataset["train"]

wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent="your_app_name/1.0")
nlp       = pipeline('question-answering', model=model_name, tokenizer=model_name)
model     = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)



done = set()

def get_gt_infobox():
    pass

def get_llm_infobox():
    pass

def score(res_gt,res_llm):
    pass

csv_file = "results.csv"
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)  # Create a CSV writer


for question_data in questions:
    idx = question_data["question_id"]
    if idx not in done:
        done.add(idx)

        document_title = question_data['document_title']
        question = question_data['question']

        page = wiki_wiki.page(document_title)

        if page.exists():
            url = page.fullurl

            gt_infobox  = get_gt_infobox()
            llm_infobox = get_llm_infobox()


            QA_input_gt = {
                'question': question,
                'context': gt_infobox
            }
            QA_input_llm = {
                'question': question,
                'context': llm_infobox
            }
            res_gt = nlp(QA_input_gt)
            res_llm = nlp(QA_input_llm)

            acc = score(res_gt,res_llm)

        data = [question, url, res_gt, res_llm, acc]

        writer.writerow(data)
    else:
        print("Page does not exist, damn!")



