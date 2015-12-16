import json

class InvalidCredentialsSchemaError(Exception):
    def __init__(self):
        super().__init__('Account credentials must contain an email and a password.')

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