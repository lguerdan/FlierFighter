import os
from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_extract import Lookup
import datefinder


'''This method takes the text and extracts the location'''
def extract_location(text):
    creds = authenticate()
    client = ClientBuilder(credentials).build_us_extract_api_client()
    lookup = Lookup(text)
    result = client.send(lookup)
    set_of_addresses = []
    for address in result.addresses:
        if address.verified:
            set_of_addresses.append(address)
    return set_of_addresses


def authenticate():
    os.environ['SMARTY_AUTH_ID'] = '726a71e0-04ce-d9ac-102b-29792739c6a5'
    os.environ['SMARTY_AUTH_TOKEN'] = 'ZXfEg1170g0oyImKttO0'
    auth_id = os.environ['SMARTY_AUTH_ID']  # We recommend storing your keys in environment variables
    auth_token = os.environ['SMARTY_AUTH_TOKEN']
    return StaticCredentials(auth_id, auth_token)
    # credentials = StaticCredentials(auth_id, auth_token)


'''Get date from text'''
def extractTime(text):
    matches = list(datefinder.find_dates(input_string))
    if (len(matches) > 0):
        return matches[0]