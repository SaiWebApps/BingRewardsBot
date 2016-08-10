import base64
import random

from randomwordgenerator import backup

class Password:
    def __init__(self, password, salt = None):
        '''
            @param password, salt
            The new password value to be stored in this object.
            If a salt value is specified along with @password, then password is already
            encrypted, so we just save the password and salt as is.
            Otherwise, the password is unencrypted and must be salted and encrypted before
            being stored.
        '''
        if salt:
        	self._password = password
        	self.salt = salt
        else:
            self.password = password

    @property
    def password(self):
        '''
            @return
            The encrypted password value stored within this object.
        '''
        return self._password

    @password.setter
    def password(self, unencrypted_password):
        '''
            @description
            First, salt the parameter @unencrypted_password. Then, encrypt the password-salt
            combination, and update the password value stored in this object.

            @param unencrypted_password
            Unencrypted new password value.
        '''
        num_words = random.randint(2, 10)
        word_len_bounds = (12, 20)
        self.salt = ''.join(backup.get_n_random_words(num_words, word_len_bounds))
        password_and_salt_bytes = (unencrypted_password + self.salt).encode('utf-8')
        self._password = base64.b64encode(password_and_salt_bytes).decode('utf-8')

    def __str__(self):
        '''
            @return
            The un-salted, decrypted, raw password version of the value within this object.
            In other words, the original (decrypted) password.
        '''
        password_and_salt = base64.b64decode(self._password.encode('utf-8')).decode('utf-8')
        return password_and_salt[:password_and_salt.rfind(self.salt)]