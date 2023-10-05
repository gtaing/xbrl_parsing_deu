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
        with open(file, encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        parsed_content = pd.DataFrame(process_deu(soup)['numerical_variables'])
        parsed_content['origin'] = file
    except UnicodeDecodeError as error:
        print(error)
        parsed_content = pd.DataFrame()
    return parsed_content


if __name__ == "__main__":

    parent_folder = os.path.dirname(os.getcwd())
    xblr_docs = os.listdir(os.path.join(parent_folder, 'data'))

    xblr_docs = [doc for doc in xblr_docs if doc.endswith('xhtml')]
    xblr_docs = [os.path.join(parent_folder, 'data', doc) for doc in xblr_docs]

    # Parse all xhtml files
    parsed_docs = [parse_xhtml_doc(doc) for doc in xblr_docs]

    # Write all parsed documents to Excel
    path = os.path.join(parent_folder, 'result', 'parsed_xblr.xlsx')
    writer = pd.ExcelWriter(path, engine="xlsxwriter")

    # Write each dataframe to a different worksheet.
    for doc in parsed_docs:
        sheet_name = doc['origin'].iloc[0]
        sheet_name = sheet_name.split('\\')[-1]
        sheet_name = sheet_name[:31] if len(sheet_name) > 32 else sheet_name
        print(sheet_name)
        doc.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()

