from mysql.connector import connect, Error
from time import time, sleep
import re, sys, subprocess, os
import dbStaff
import dbDistrict

def execute_query(connection, query, flag='yes'):
    global dbName
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if flag == 'no':
            re_db = re.compile(r'[a-z]{1,15}')
            if re_db.match(str(query)):
                match = str(query).split()
                dbName = str(match[2].replace('\'', ''))
                print('Database Created\n')
                return

            print('\n* Improper database naming => {} .. 15 string character limit.. *'.format(query))
            sleep(4)
            sys.exit(3) 

        print('Query successful\n')
        return

    except Error as err:
        print('\nError: {}'.format(err))
        sleep(4)
        sys.exit(2)

def init_connection(hostname, username, flag='yes', database=None):
    global dbName
    try:
        if flag == 'no':
            connection = connect(host=hostname, user=username)
            print('MySQL Database connection successfull')
            return connection

        connection = connect(host=hostname, user=username, database=dbName)
        print('MySQL Database connected')
        return connection

    except Error as err:
        print('\nError: {}'.format(err))
        sleep(4)
        sys.exit(1)

def query_handler(db, table , alt, pop):
    connection = init_connection('localhost', 'root', 'no')
    db_init = execute_query(connection, bytes(db, 'utf-8'), 'no')

    for tFunc in table[:]:
        print(tFunc)
        connection = init_connection('localhost', 'root', db_init)
        execute_query(connection, bytes(tFunc, 'utf-8'))

    for aFunc in alt[:]:
        print(aFunc)
        connection = init_connection('localhost', 'root', db_init)
        execute_query(connection, bytes(aFunc, 'utf-8'))

    for pFunc in pop[:]:
        print(pFunc)
        connection = init_connection('localhost', 'root', db_init)
        execute_query(connection, bytes(pFunc, 'utf-8'))

    return

def main():
    start = time()
    # Establish MySQL data sets to be imported from external files #
    databases = ( dbStaff.staffDatabase, dbDistrict.districtDatabase )
    tables = ( dbStaff.staffTables, dbDistrict.districtTables )
    alters = ( dbStaff.staffAlterations, dbDistrict.districtAlterations )
    populates = ( dbStaff.staffPopulate, dbDistrict.districtPopulate )

    # Create databases & tables, make modifications, and populate tabels #
    for db, table, alt, pop in zip(databases, tables, alters, populates):
        query_handler(db, table, alt, pop)

    # Select number of users #
    while True:
        os.system('cls')
        try:
            user_num = int(input('How many users would you like to add (1-12)? '))

        except ValueError:
            print('* Incorrect data type .. enter number *')
            sleep(4)
            continue

        if 1 <= user_num <= 12:
            break

        print('\n* Invalid input .. enter 1 to 12 users *')
        sleep(4)
        continue

    # Create username/password #
    re_user = re.compile(r'^[a-zA-z_]{3,15}')
    re_pass = re.compile(r'^[a-zA-Z0-9!@_$(]{12,24}')
    usernames = []
    while user_num != 0:
        while True:
            os.system('cls')
            user = input('Enter name for user:\n(3 to 15 charaters with underscores allowed) => ')
            password = input('\nEnter a password for user => {}:\n'
                             '(12-24 charaters, !(@_$ meta characters allowed) => '.format(user))
            pass_check = input('\nConfirm entered password => ')

            if password == pass_check:
                if re_user.match(user) and re_pass.match(password):
                    break

                print('\n* Incorrect user/password formatting *')
                sleep(4)
                continue

            print('\n* Passwords do not match *')
            sleep(4)
            continue

        usernames.append({user:password})
        user_num -= 1

    # Select privilege level #
    options = ['ALL', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'EXECUTE']
    for username in usernames:
        for key,value in username.items():
            while True:
                os.system('cls')   
                print('Priviledge options => {}'.format(', '.join(options)))
                grant = input('Enter user privilege:\n')
                flag = 'off'
                for option in options:
                    if grant == option:
                        flag = 'on'
                        break
                    else:
                        pass

                if flag == 'on':
                    break

                print('\n* Select one of the options provided *')
                sleep(4)
                continue

            # Select where to apply privilege: globally, database or table level #
            re_validate = re.compile(r'^(?:\*\.\*|[a-zA-Z0-9_]{3,15}\.(?:[a-zA-Z0-9_]{3,15}|\*))')
            while True:
                os.system('cls')
                print('Assign privilege globaly(*.*), database(db.*), or table(db.example)')
                on = input('Enter the database(s) or table(s) to assign privilege:\n')

                if not re_validate.match(on):
                    print('\n* Incorrect formatting .. database names may be 3 to 15' 
                          'letters, numbers or underscore separators *')
                    sleep(4)
                    continue

                try:
                    connection = connect(host='localhost', user='root')
                    cursor = connection.cursor()
                    cursor.execute('''CREATE USER\"{}\"@\"localhost\" IDENTIFIED BY \"{}\";
                                      GRANT {} ON {} TO \"{}\"@\"localhost\";
                                   '''.format(key, value, grant, on, key), multi=True)
                    connection.commit()
                    break

                except Error as err:
                    print('\nError: {}'.format(err))
                    sleep(4)
                    continue

    print(time() - start)


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('\n* Ctrl + C detected .. Exiting *')