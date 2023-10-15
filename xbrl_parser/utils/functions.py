import pandas as pd


def extract_period(tag):
    """

    :param tag:
    :return:
    """
    if tag.find_all('xbrli:instant'):
        period = {
            "instant": tag.find_all('xbrli:instant')[0].string
        }

    else:
        period = {
            "startdate": tag.find_all('xbrli:startdate')[0].string,
            "enddate": tag.find_all('xbrli:enddate')[0].string
        }

    return period


def extract_dimensions(tag):
    """

    :param tag:
    :return:
    """
    dimensions = {}

    for dimension in tag.find_all('xbrldi:explicitmember'):
        dimensions[dimension.attrs['dimension']] = dimension.string

    return dimensions


def parse_context(soup):
    """

    :param soup:
    :return:
    """
    xbrli_contexts = soup.find_all('xbrli:context')

    parsed_xbrli_contexts = []

    for tag in xbrli_contexts:
        parsed_xbrli_contexts.append({
            "ID": tag.attrs['id'],
            "period": extract_period(tag),
            "dimensions": extract_dimensions(tag)})

    return pd.DataFrame(parsed_xbrli_contexts)


def flatten_dates_from_period(contexts):
    """

    :param contexts:
    :return:
    """
    return pd.concat([contexts, contexts['period'].apply(pd.Series)], axis=1)


def flatten_dimensions(contexts):
    """

    :param contexts:
    :return:
    """
    return pd.concat([contexts, contexts['dimensions'].apply(lambda x: pd.Series(x, dtype='object'))], axis=1)


def parse_numerical_variables(soup):
    """

    :param soup:
    :return:
    """
    ix_nonfraction = soup.find_all('ix:nonfraction')
    parsed_ix_nonfraction = []

    for tag in ix_nonfraction:
        # sometimes we don't have a format for a numeric fact
        if "format" not in tag.attrs:
            tag['format'] = "UNDEFINED"

        parsed_tag = {
            "ID": tag["contextref"],
            "decimals": tag["decimals"],
            "name": tag["name"],
            "format": tag["format"],
            "scale": tag["scale"],
            "value": tag.string
        }

        parsed_ix_nonfraction.append(parsed_tag)

    return pd.DataFrame(parsed_ix_nonfraction)


def parse_variable_name(data):
    """

    :param data:
    :return:
    """
    data['name'] = data['name'].apply(lambda x: x.split(':')[1])
    return data


def compute_real_value(data):
    """

    :param data:
    :return:
    """
    data['real_value'] = data['value'].copy()

    data['real_value'] = data['real_value'].apply(lambda x: x.replace(' ', '').replace(',', '.').replace('\xa0', ''))
    data['real_value'] = data['real_value'].replace('‐', 0)
    data['real_value'] = data['real_value'].replace('-', 0)

    #data['real_value'] = data['real_value'].astype('float')

    #data['real_value'] = (10 ** data['scale'].astype(int)) * data['real_value']

    return data


def parse_text_variables(soup):
    """

    :param soup:
    :return:
    """
    ix_nonnumeric = soup.find_all('ix:nonnumeric')
    parsed_ix_nonnumeric = []

    for tag in ix_nonnumeric:
        parsed_tag = {
            "ID": tag["contextref"],
            "name": tag["name"],
            "value": tag.text
        }

        parsed_ix_nonnumeric.append(parsed_tag)

    return pd.DataFrame(parsed_ix_nonnumeric)


def process_contexts(soup):
    """

    :param soup:
    :return:
    """
    contexts = parse_context(soup)
    contexts = flatten_dates_from_period(contexts)
    contexts = flatten_dimensions(contexts)
    contexts = contexts.drop(columns=['period', 'dimensions'])
    return contexts


def process_numerical_variables(soup):
    """

    :param soup:
    :return:
    """
    numerical_variables = parse_numerical_variables(soup)
    numerical_variables = compute_real_value(numerical_variables)

    return numerical_variables


def process_text_variables(soup):
    """

    :param soup:
    :return:
    """
    text_variables = parse_text_variables(soup)

    return text_variables


def process_deu(soup):
    """

    :param soup:
    :return:
    """
    contexts = process_contexts(soup)
    numerical_variables = process_numerical_variables(soup)
    text_variables = process_text_variables(soup)

    return {
        "contexts": contexts,
        "numerical_variables": numerical_variables,
        "text_variables": text_variables
    }
