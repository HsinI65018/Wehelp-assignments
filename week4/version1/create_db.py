from turtle import home
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='password'
)

my_cursor = mydb.cursor()

my_cursor.execute('CREATE DATABASE week4;')

my_cursor.close()
mydb.close()