# Quickly connects to RDS instance and performs 50 sets of table inserts with 10 entries and 5 secs wait time

import mysql.connector
from mysql.connector import MySQLConnection, Error

import time

#  TODO: put all the functions under a class
def main(host_name,db_name,user_name,db_password):
    conn = None

    try:
        main.conn = mysql.connector.connect(host=host_name, database=db_name, user=user_name, password=db_password)

        if main.conn.is_connected():
            print('Inserting stuffs... ')
            insert_stuff()

    except Error as e:
        print(e)


def insert_stuff():
    mycursor = main.conn.cursor()

    sql = "INSERT INTO example (id, name) VALUE (%s, %s)"
    value = ("Test", "Example1")

    i = 0
    x = 0
    totalrows = 0

    for i in range(0,50):
        for x in range(0,10):
            mycursor.execute(sql, value)
            main.conn.commit()
            totalrows += mycursor.rowcount
            #print(str(x) + " inner round completed")
        print(str(i) + " round completed")
        time.sleep(5)

    if mycursor.close() == True:
        print("Total row inserted: {}".format(totalrows))
        return main.conn.close()
    else:
        print("Something is wrong")

if __name__ == '__main__':
    host_name = input('Enter RDS hostname: ')
    db_name = input('Enter DB name: ')
    user_name = input('Enter username: ')
    db_password = input('Enter password: ')
    main(host_name, db_name, user_name, db_password)
