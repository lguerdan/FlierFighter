import os
from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_extract import Lookup
import datefinder
import nltk
from nameparser.parser import HumanName


'''This method takes the text and extracts the location'''
def extract_location(text):
    # creds = authenticate()
    creds = StaticCredentials('726a71e0-04ce-d9ac-102b-29792739c6a5', 'ZXfEg1170g0oyImKttO0')
    client = ClientBuilder(creds).build_us_extract_api_client()
    lookup = Lookup(text)
    result = client.send(lookup)
    print text
    print result.addresses
    set_of_addresses = []
    if len(result.addresses) > 0:
        for address in result.addresses:
            if address.verified:
                set_of_addresses.append(address)
    return set_of_addresses


def authenticate():
    # os.environ['SMARTY_AUTH_ID'] = '726a71e0-04ce-d9ac-102b-29792739c6a5'
    # os.environ['SMARTY_AUTH_TOKEN'] = 'ZXfEg1170g0oyImKttO0'
    # auth_id = os.environ['SMARTY_AUTH_ID']  # We recommend storing your keys in environment variables
    # auth_token = os.environ['SMARTY_AUTH_TOKEN']
    return StaticCredentials(auth_id, auth_token)
    # credentials = StaticCredentials(auth_id, auth_token)


'''Get date from text'''
def extractTime(text):
    matches = list(datefinder.find_dates(input_string))
    if (len(matches) > 0):
        return matches[0]


'''Get names from text'''
def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.node == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: # avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return (person_list)