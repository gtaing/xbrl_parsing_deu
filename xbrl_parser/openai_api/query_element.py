import os
import openai
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

openai.api_key = 'YOUR_API_KEY'


def extract_text_from_xhtml(xhtml_path):
    with open(xhtml_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text()
    return text


def read_specific_page(file_path, page_number):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Assuming each page is enclosed in a 'div' tag with class 'S0'
    pages = soup.find_all('div', class_='S0')

    if page_number <= len(pages):
        specific_page = pages[page_number - 1].get_text()
        return specific_page
    else:
        return f"Page {page_number} does not exist in the file."


def read_continuous_pages(file_path, page_start_number, page_stop_number):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Assuming each page is enclosed in a 'div' tag with class 'S0'
    pages = soup.find_all('div', class_='S0')

    text = ''
    for page_number in tqdm(np.arange(page_start_number, page_stop_number)):
        text += pages[page_number - 1].get_text()
    return text


def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # or another available engine
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()


if __name__ == "__main__":
    parent_folder = os.path.dirname(os.getcwd())
    path = os.path.join(os.path.dirname(parent_folder), 'data', 'Fnac_Darty.xhtml')
    extracted_text = read_continuous_pages(file_path=path,
                                           page_start_number=21,
                                           page_stop_number=24)

    # Dump text file to query chatGPT using the web interface
    with open('text_dump.txt', 'w', encoding="utf-8") as f:
        f.write(extracted_text)

    # Query ChatGPT API with query
    txt_prompt = "Quelles sont les objectifs de réduction pour les émissions de CO2 : " + extracted_text
    response = chat_with_gpt(prompt=txt_prompt)

    with open('openai_response.txt', 'w', encoding="utf-8") as f:
        f.write(response)

