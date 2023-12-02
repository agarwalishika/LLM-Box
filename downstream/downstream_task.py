from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from datasets import load_dataset
import pandas as pd
from rouge_score import rouge_scorer
import csv

model_name= "deepset/roberta-base-squad2"

nlp       = pipeline('question-answering', model=model_name, tokenizer=model_name)
model     = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


csv_file_path = 'downstream_questions.csv'
questions = {}

with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if int(row[0]) not in questions.keys():
            questions[int(row[0])] = []
        questions[int(row[0])].append(row[1])

scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
data = []
for i in questions.keys():
    for q in questions[i]:
        for j in range(50):
            idx = i*10 + j

            with open(f"articles/generated_infoboxes/ground_truth/{idx}.txt","r",encoding="latin-1") as gt:
                with open(f"articles/generated_infoboxes/llm_box/{idx}.txt","r",encoding="latin-1") as llm:
                    infobox_gt = "".join(gt.readlines())
                    infobox_llm = "".join(llm.readlines())

                    QA_input_gt = {
                                    'question': q,
                                    'context': infobox_gt
                                }

                    res_gt_raw= nlp(QA_input_gt)
                    score_gt = res_gt_raw['score']
                    res_gt = res_gt_raw['answer']
                    

                    
                    QA_input_llm = {
                        'question': q,
                        'context': infobox_llm
                    }
                        
                    res_llm_raw = nlp(QA_input_llm)
                    score_llm = res_llm_raw['score']
                    res_llm = res_llm_raw['answer']


                    acc = scorer.score(res_gt,res_llm)


                    data.append([idx,q,  res_gt, res_llm, acc,score_gt,score_llm])
                    
