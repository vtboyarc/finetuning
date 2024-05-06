import json
import requests
import os

def query_ollama(prompt, model='mistral', context=''):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": model,
            "stream": False,
            "prompt": context + prompt
        }
    )
    if response.status_code != 200:
        raise Exception('API call failed: ' + response.text)
    return response.json()['response'].strip()

def create_valid_file():
    if not os.path.exists('train.jsonl'):
        raise Exception('No train.jsonl file found!')

    with open('train.jsonl', 'r') as file:
        train_lines = file.readlines()

    # Remove 20% of the training data and put it into a validation file
    total_lines = len(train_lines)
    twenty_percent = round(total_lines * 0.2)
    val_lines = train_lines[:twenty_percent]
    train_lines = train_lines[twenty_percent:]

    with open('train.jsonl', 'w') as file:
        file.writelines(train_lines)

    with open('valid.jsonl', 'w') as file:
        file.writelines(val_lines)

if not os.path.exists('instructions.json'):
    raise Exception('Please provide an instructions.json file to get started.')

with open('instructions.json', 'r') as file:
    instructions = json.load(file)

total = len(instructions)
print("------------------------------")
for i, instruction in enumerate(instructions, start=1):
    print(f"({i}/{total}) {instruction}")
    print("------------------------------")

    answer = query_ollama(instruction)
    print(answer)

    result = {'text': f'<s>[INST] {instruction}[/INST] {answer}</s>'}
    output = json.dumps(result) + "\n"
    output = output.replace('[\/INST]', "[/INST]").replace('<\/s>', "</s>")

    print("\n\n------------------------------\n")

    with open('train.jsonl', 'a') as file:
        file.write(output)

create_valid_file()

print("Done! Training and validation JSONL files created.")
