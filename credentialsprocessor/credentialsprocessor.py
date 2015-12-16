import argparse
import json

import accountcredentialsmodels

# Utility Methods to Convert b/w JSON files and AccountCredentials objects
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
        password_list = [json_obj['password'] for json_obj in json_credentials]
        return accountcredentialsmodels.AccountCredentialsCollection(email_list, password_list)

def save_credentials(filename, email_addresses, passwords, delimiter = ','):
    '''
        @description
        Save the given set of credentials into an AccountCredentialsCollection object, which will
        in turn be written to a file with the given name. If a file already exists for the given
        filename, it shall be overwritten.

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
    password_list = [p.strip() for p in passwords.split(delimiter)]
    creds_collection = accountcredentialsmodels.AccountCredentialsCollection(email_address_list, password_list)
    creds_collection.print_to_json_file(filename)

# Main Method
def main():
    parser = argparse.ArgumentParser(description = 'Process Bing-Rewards accounts\' credentials')
    parser.add_argument('-f', '--filename', required = False, help = \
        'Name of the JSON file that the credentials are/will be stored in.')
    parser.add_argument('-e', '--email_addresses', required = False, help = \
        'Comma-separated list of email addresses.')
    parser.add_argument('-p', '--passwords', required = False, help = \
        'Comma-separated list of passwords corresponding to each email address specified with "-e".')

    args = parser.parse_args()
    if args.filename and args.email_addresses and args.passwords:
        save_credentials(args.filename, args.email_addresses, args.passwords)
    elif args.filename and not args.email_addresses and not args.passwords:
        print(str(process_credentials(args.filename)))
    else:
        raise ValueError('Must specify either filename alone or filename + BOTH email addresses and passwords')

if __name__ == '__main__':
    main()