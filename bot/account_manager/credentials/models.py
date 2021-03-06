class AccountCredentials:
    def __init__(self, email, password):
        '''
            @description
            Constructor - creates an object with the account credentials for a Bing Rewards account.

            @param email
            Email address of Bing Rewards account.

            @param password
            Encrypted password of Bing Rewards account; an instance of the simplesecurity.Password class.
        '''
        self.email = email
        self.password = password

    def to_std_structure(self):
        return {'email': self.email, 'salt': self.password.salt, 'password': self.password.password}

class AccountCredentialsCollection:
    def __init__(self, email_list, password_list):
        '''
            @param email_list
            List of Bing Rewards accounts' email addresses

            @param password_list
            - List of encrypted Bing Rewards accounts' passwords (simplesecurity.Password objects).
            - The size of this list SHALL equal that of email_list
        '''
        num_creds = len(email_list)
        self.credentials_collection = [AccountCredentials(email_list[i], password_list[i]) for i in range(0, num_creds)]

    def to_std_structure(self):
        return [obj.to_std_structure() for obj in self.credentials_collection]

    def size(self):
        return len(self.to_std_structure())