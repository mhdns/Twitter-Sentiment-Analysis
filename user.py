from database import ConnectionPool
from twitter_utils import *
import json

class User:
    def __init__(self, screen_name, oauth, oauth_secret, id = None):
        self.screen_name = screen_name
        self.oauth = oauth
        self.oauth_secret = oauth_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.screen_name)

    def save_to_db(self):
        with ConnectionPool() as cursor:
            cursor.execute("INSERT INTO users (screen_name, oauth, oauth_secret) VALUES (%s, %s, %s)",
                           (self.screen_name, self.oauth, self.oauth_secret))

    def twitter_request(self, url):
        user_token = oauth2.Token(self.oauth, self.oauth_secret)
        client = oauth2.Client(consumer, user_token)
        response, content = client.request(url)
        if response.status != 200:
            return "ERROR!!!"
        return json.loads(content.decode("UTF-8"))


    @classmethod
    def load_from_db(cls, screen_name):
        with ConnectionPool() as cursor:
            cursor.execute("SELECT * FROM users WHERE screen_name = %s;", (screen_name,))
            user = cursor.fetchone()
            if user:
                return User(user[0], user[1], user[2], user[3])

    @classmethod
    def laod_all_data(cls):
        all_users = []
        with ConnectionPool() as cursor:
            cursor.execute("SELECT * FROM users;")
            rows = cursor.fetchall()
            if rows:
                for user in rows:
                    all_users.append(User(user[0], user[1], user[2], user[3]))
        return all_users

