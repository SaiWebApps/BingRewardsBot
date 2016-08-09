from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from accountcredentialsmodels import AccountCredentialsCollection
from simplesecurity import Password

'''
    SQL-lite Database-Related Utilities
'''
_credentials_table = Table('credentials', MetaData(), \
    Column('credentials_id', Integer, primary_key = True, autoincrement = True), \
    Column('email', String), \
    Column('password', String), \
    Column('salt', String))

# Database Management Decorator
def _manage_database_connection(function):
    '''
        @param function
        Function being wrapped by this decorator.
    '''
    def func_wrapper(db, *args, **kwargs):
        '''
            @param db
            Initially the name of the database file that we will opening
            a connection to and modifying.
            Will be changed to the database connection within this decorator.
        '''
        # Open database connection to the specified database file.
        db_engine = create_engine('sqlite:///' + db)
        _credentials_table.create(db_engine, checkfirst = True)
        db_conn = db_engine.connect()
        
        # db is initially the database file name.
        # Replace it now with the database connection.
        db = db_conn

        # Execute the function.
        function_output = function(db, *args, **kwargs)

        # Close connection now that we're        
        db_conn.close()

        return function_output
    return func_wrapper

# Credentials Table Utility Functions
@_manage_database_connection
def _save_credentials(db, credentials_collection):
    '''
        @param db
        User specifies the database file name.
        The decorator, _manage_database_connection, will open a connection to the
        specified database file and replace this value with the connection instead.

        @param credentials_collection
        AccountCredentialsCollection object
    '''
    db.execute(_credentials_table.insert(), credentials_collection.to_std_structure())

@_manage_database_connection
def _get_all_credentials(db):
    '''
        @param db
        User specifies the database file name.
        The decorator, _manage_database_connection, will open a connection to the
        specified database file and replace this value with the connection instead.

        @return
        A list of dictionaries, where each dict contains the info from a row in
        _credentials_table.
    '''
    return [{'email': creds.email, 'password': creds.password, 'salt': creds.salt} \
        for creds in db.execute(_credentials_table.select())]

'''
    Publically Exposed Credentials Management Functions
'''
def process_credentials(filename):
    '''
        @param filename
        Name of the database file with the credentials info that we want to load
        into an AccountCredentialsCollection object.

        @return
        AccountCredentialsCollection object with the credentials info in the
        given database file.
    '''
    all_creds = _get_all_credentials(filename)
    email_address_list = [c['email'] for c in all_creds]
    password_list = [Password(c['password'], c['salt']) for c in all_creds]
    return AccountCredentialsCollection(email_address_list, password_list)

def save_credentials(filename, email_addresses, passwords, delimiter = ','):
    '''
        @param filename
        Name of the database file in which we want to save the provided credentials info.

        @param email_addresses, passwords
        Delimited strings containing credentials info that we want to load into a database.
        Once we split on the delimiter, there should be an equal # of email address and
        password tokens.

        @param delimiter
        Character that is separating the individual email addresses and passwords from each other
        in the provided strings.

        @return
        AccountCredentialsCollection with the provided credentials info, which has also been
        saved to the specified database file.
    '''
    email_address_list = [addr.strip() for addr in email_addresses.split(delimiter)]
    # Salt and encrypt provided passwords.
    password_list = [Password(p.strip()) for p in passwords.split(delimiter)]
    creds_collection = AccountCredentialsCollection(email_address_list, password_list)
    _save_credentials(filename, creds_collection)
    return creds_collection