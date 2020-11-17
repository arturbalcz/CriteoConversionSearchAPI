import mysql.connector as connector


def connect_to_db(host='localhost', user='root', password='q1w2e3r4', port='33069'):
    return connector.connect(host=host, port=port, password=password, user=user, database='ccs')
