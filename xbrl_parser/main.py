import os
import pandas as pd
from bs4 import BeautifulSoup
from xbrl_parser.utils.functions import process_deu


def parse_xhtml_doc(file):
    """

    :param file:
    :return:
    """
    try:
        with open(file) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        parsed_content = process_deu(soup)
    except UnicodeDecodeError:
        parsed_content = pd.DataFrame()
    return parsed_content


if __name__ == "__main__":

    parent_folder = os.path.dirname(os.getcwd())
    xblr_docs = os.listdir(os.path.join(parent_folder, 'data'))

    xblr_docs = [doc for doc in xblr_docs if doc.endswith('xhtml')]
    xblr_docs = [os.path.join(parent_folder, 'data', doc) for doc in xblr_docs]

    # Parse all xhtml files
    parsed_docs = [parse_xhtml_doc(doc) for doc in xblr_docs]
    print(parsed_docs)





