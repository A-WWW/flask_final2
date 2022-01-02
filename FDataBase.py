import sqlite3
import time
import math
import re
from flask import Flask, render_template, request, g, flash, url_for

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Что-то пошло не так")
        return []

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Что-то пошло не так" + str(e))
            return False

        return True

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Что-то пошло не так " + str(e))

        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Что-то пошло не так " + str(e))

        return []

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("You are already registered")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Add error" + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not found")
                return False
            return res
        except sqlite3.Error as e:
            print("Что-то пошло не так " + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = {email} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not found")
                return False
            return res
        except sqlite3.Error as e:
            print("Что-то пошло не так " + str(e))

        return False