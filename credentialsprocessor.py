import argparse
import json

# Custom Exception Class
class InvalidCredentialsSchemaError(Exception):
    def __init__(self):
        super().__init__('Account credentials must contain an email and a password.')

# Account Credentials Objects
class AccountCredentials:
    def __init__(self, email, password):
        '''
            @description
            Constructor - creates an object with the account credentials for a Bing Rewards account.

            @param email
            Email address of Bing Rewards account

            @param password
            Password of Bing Rewards account
        '''
        self.email = email
        self.password = password

    def to_dict(self):
        '''
            @description
            Converts this AccountCredentials object into a Python dictionary.

            @return
            {'email': value of email field in this AccountCredentials object,
            'password': value of password field in this AccountCredentials object}
        '''
        return {'email': self.email, 'password': self.password}

    def __str__(self):
        '''
            @return the following JSON string:
            {
                'email': this AccountCredentials object's email field,
                'password': this AccountCredentials object's password field
            }
        '''
        return json.dumps(self.to_dict(), sort_keys = True, indent = 4, separators = (',', ':'))

    def print_to_json_file(self, filename):
        '''
            @description
            Similar to __str__, except instead of returning a JSON string, we are writing the
            string to the specified file.

            @param filename
            Name of the file to which we are writing the JSON string of this object.
        '''
        with open(filename, 'w') as json_file_ptr:
            json.dump(self.to_dict(), json_file_ptr, sort_keys = True, indent = 4, separators = (',', ':'))

class AccountCredentialsCollection:
    def __init__(self, email_list, password_list):
        '''
            @param email_list
            List of Bing Rewards accounts' email addresses

            @param password_list
            List of Bing Rewards accounts' passwords; the size of this list SHALL equal that of email_list
        '''
        if len(email_list) != len(password_list):
            raise InvalidCredentialsSchemaError
        num_creds = len(email_list)
        self.credentials_collection = [AccountCredentials(email_list[i], password_list[i]) for i in range(0, num_creds)]

    def to_collection_of_dicts(self):
        '''
            @description
            Convert the list of AccountCredentials objects in this container into a list of
            Python dictionaries.
        '''
        return [creds_obj.to_dict() for creds_obj in self.credentials_collection]

    def __str__(self):
        '''
            @return the following JSON string:
            [
                {
                    'email': AccountCredentials object 1's email field
                    'password': AccountCredentials object 1's password field
                },
                .... -> Continue for remaining AccountCredentials objects in this container
            ]
        '''
        return json.dumps(self.to_collection_of_dicts(), sort_keys = True, indent = 4, separators = (',', ':'))

    def print_to_json_file(self, filename):
        '''
            @description
            Similar to __str__, except instead of returning a JSON string, we are writing the
            string to the specified file.

            @param filename
            Name of the file to which we are writing the JSON string of this object.
        '''
        with open(filename, 'w') as json_file_ptr: 
            json.dump(self.to_collection_of_dicts(), json_file_ptr, sort_keys = True, indent = 4, separators = (',', ':'))

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
        return AccountCredentialsCollection(email_list, password_list)

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
    creds_collection = AccountCredentialsCollection(email_address_list, password_list)
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