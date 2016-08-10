import json

from models import AccountCredentialsCollection
from simplesecurity import Password

def process_credentials(filename):
    '''
        @description
        Load the information in the given JSON file into an AccountCredentialsCollection object.

        @param filename
        Name of the JSON file that we are converting into an AccountCredentialsCollection object

        @return
        An AccountCredentialsCollection object with the credentials in the given JSON file.
    '''
    with open(filename, 'r') as json_file_ptr:
        json_credentials = json.load(json_file_ptr)
        email_list = [json_obj['email'] for json_obj in json_credentials]
        password_list = [Password(json_obj['password'], json_obj['salt']) for json_obj in json_credentials]
        return AccountCredentialsCollection(email_list, password_list)

def save_credentials(filename, email_addresses, passwords, delimiter = ','):
    '''
        @description
        Save the given set of credentials into an AccountCredentialsCollection object, which will
        in turn be written to a file with the given name. If a file already exists for the given
        filename, the provided creds info will be appended to it.

        @param filename
        Name of the JSON file in which the given email addresses and passwords will be stored.

        @param email_addresses, passwords
        The account credentials information for a set of Bing-Rewards accounts; will be saved to
        an AccountCredentialsCollection object, which will in turn be written to a JSON file
        called filename.

        @param delimiter
        The separator between email addresses and passwords (e.g., a comma).
    '''
    email_address_list = [addr.strip() for addr in email_addresses.split(delimiter)]
    password_list = [Password(p.strip()) for p in passwords.split(delimiter)]
    creds_collection = AccountCredentialsCollection(email_address_list, password_list)
    with open(filename, 'a') as json_file_ptr:
    	json.dump(creds_collection.to_std_structure(), json_file_ptr, sort_keys = True, indent = 4, separators = (',', ':'))
    return process_credentials(filename)