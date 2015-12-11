import argparse
import json

class AccountCredentials:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_dict(self):
        return {'email': self.email, 'password': self.password}

    def to_tuple(self):
        return (self.email, self.password)

    def __str__(self):
        return json.dumps(self.to_dict())

class InvalidCredentialsSchemaError(Exception):
    def __init__(self):
        super().__init__('Account credentials must contain an email and a password.')

def process_credentials(filename):
    json_file = None
    try:
        json_file = open(filename, 'r')
        json_credentials = json.load(json_file)
        return [AccountCredentials(json_obj['email'], json_obj['password']) for json_obj in json_credentials]
    except:
        raise InvalidCredentialsSchemaError
    finally:
        if json_file:
            json_file.close()

def save_credentials(filename, email_address_list, password_list):
    json_file = None
    try:
        json_file = open(filename, 'w')
        account_cred_obj_list = [\
            AccountCredentials(email_address, password_list[index]).to_dict() \
            for index, email_address in enumerate(email_address_list)\
        ]
        json.dump(account_cred_obj_list, json_file)
    except:
        raise InvalidCredentialsSchemaError
    finally:
        if json_file:
            json_file.close()

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
        save_credentials(args.filename, args.email_addresses.split(','), args.passwords.split(','))
    elif args.filename and not args.email_addresses and not args.passwords:
        print([str(obj) for obj in process_credentials(args.filename)])
    else:
        raise ValueError('Must specify either filename alone or filename + BOTH email addresses and passwords')

if __name__ == '__main__':
    main()