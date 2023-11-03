"""
1. create a directory for each reviewer based on name.
2. define loop that keeps going when you type continue, and ends when you type end
3. when you type continue:
    picks a random directory between "ground_truth" and "llm_box"
    starting with file 0
    create the html file for the infobox
    open the html file in a browser
    create a feedback file with 3 prompts in it
    person fills out prompt and closes the file.
    types "continue" or "end" in the terminal.
    the file number and label for the feedback is appended
    increment file counter
"""
import os
import random
import webbrowser 

## CHANGE ME:
REVIEWER_NAME = "Siddharth"

## DO NOT CHANGE BELOW THIS LINE
labels = ["ground_truth", "llm_box"]
questions = [
    "(1) Is all the information in the infobox accurate to the information in the article? Please identify any potential discrepancies.",
    "(2) On a scale of 1 to 10, where 1 is too verbose and 10 is too concise, please rate the field values on their succinctness.",
    "(3) Please list any additional fields you would have added to the infobox to make it a more holistic summary of the article, if any"
]

beginning_html =  """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    .infobox {
        --font-size-medium: 0.875rem;
        font-family: sans-serif;
        direction: ltr;
        border: 1px solid #a2a9b1;
        background-color: #f8f9fa;
        color: black;
        margin: 0.5em 0 0.5em 1em;
        padding: 0.2em;
        float: right;
        clear: right;
        font-size: 88%;
        line-height: 1.5em;
        width: 22em;
        border-spacing: 2px 5px;
    }

    tbody {
        --font-size-medium: 0.875rem;
        font-family: sans-serif;
        direction: ltr;
        color: black;
        font-size: 88%;
        line-height: 1.5em;
        border-spacing: 2px 5px;
    }

    tr {
        --font-size-medium: 0.875rem;
        font-family: sans-serif;
        direction: ltr;
        color: black;
        font-size: 88%;
        line-height: 1.5em;
        border-spacing: 2px 5px;
    }

    .infobox-label {
        --font-size-medium: 0.875rem;
        font-family: sans-serif;
        direction: ltr;
        color: black;
        font-size: 88%;
        line-height: 1.5em;
        border-spacing: 2px 5px;
        vertical-align: top;
        text-align: left;
    }

    .infobox-data {
        --font-size-medium: 0.875rem;
        font-family: sans-serif;
        direction: ltr;
        color: black;
        font-size: 88%;
        line-height: 1.5em;
        border-spacing: 2px 5px;
        vertical-align: top;
        text-align: left;
    }
    </style>
    <table class="infobox" style="border-spacing: 2px 5px;">
        <tbody>
    """
ending_html =  """
        </tbody> 
    </table>
    """

row_template = """
    <tr>
        <th scope="row" class="infobox-label">{key}</th>

        <td class="infobox-data">
            <span>{value}</span>
        </td>
    </tr> 
    """
def setup_review():
    if not os.path.exists(os.path.join(os.getcwd(),"manual_eval",REVIEWER_NAME)):
        os.makedirs(os.path.join(os.getcwd(),"manual_eval",REVIEWER_NAME))

def review_loop():
    i = 0

    user_prompt_string = """Thank you for reviewing!\n 
    We have created a file named 'feedback_{i}' for you under 'manual_eval/{reviewer}/'\n 
    Please view the infobox in your browser and answer the question in the feedback doc.\n 
    You will have to open the wikipedia article for the infobox subject to answer the questions.\n 
    When you are finished, close the feedback doc and type in the terminal 'continue' to proceed or 'end' to finish."""
    label = select_label()
    start_new_review(i, label)
    print(user_prompt_string.format(i=i, reviewer=REVIEWER_NAME))

    while True:
        user_input = input("Type 'continue' to proceed or 'end' to stop: ")
        if user_input.lower() == "continue":
            finish_single_review(i, label)
            i += 1
            label = select_label()
            start_new_review(i, label)
            print(user_prompt_string.format(i=i, reviewer=REVIEWER_NAME))
            # The loop will continue
        elif user_input.lower() == "end":
            finish_single_review(i, label)
            print("Ending the review session. Thank you for participating.")
            break  # This will end the loop
        else:
            print("Invalid input. Please try again. Type 'continue' to proceed or 'end' to stop:")


def finish_single_review(rev_num, label):
    with open(os.path.join(os.getcwd(),"manual_eval",REVIEWER_NAME,f'feedback_{rev_num}.txt'),"+a") as file:
        file.write(f'{rev_num} {label}')

def start_new_review(rev_num, label):
    with open(os.path.join(os.getcwd(),"manual_eval",REVIEWER_NAME,f'feedback_{rev_num}.txt'),"+w") as file:
        for q in questions:
            file.write(f'{q}\n\n')
    
    generate_visual_infobox(rev_num, label)
    

def select_label():
    return random.choice(labels)

def generate_visual_infobox(rev_num, label):
    with open(os.path.join(os.getcwd(), "articles", "generated_infoboxes",label,f"{rev_num}.txt")) as file:
        lines = file.readlines()
        with open(os.path.join(os.getcwd(), "manual_eval", "temp.html"), "+w") as html_file:
            html_file.write(beginning_html)
            for line in lines:
                if line.startswith("|"):
                    line = line.replace("|","")
                    parts = line.split("   ") if label == "ground_truth" else line.split(" = ")
                    key = parts[0]
                    value = parts[1]
                    html_file.write(row_template.format(key=key, value=value))

            html_file.write(ending_html)
    webbrowser.open(os.path.join(os.getcwd(), "manual_eval", "temp.html")) 


if __name__ == "__main__":
    setup_review()
    review_loop()
   



   


    