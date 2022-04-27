import requests
from requests_oauthlib import OAuth1
import sys
from datetime import datetime,timezone
import time
import sqlite3





usernames = sys.argv
tweets_to_db = []

    # SAVING TO SQL DATABASE
def save_tweets_to_db(to_save, user):
    conn = sqlite3.connect('tweets_database.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS usernames (username TEXT, UNIQUE (username))")
    c.execute("INSERT OR IGNORE INTO usernames(username) VALUES (?)", [user])
    c.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
        tweet_id integer PRIMARY KEY,
        username TEXT,
        date_tweet TEXT,
        text_tweet TEXT,
        FOREIGN KEY (username) REFERENCES usernames (username)
    )""")
    c.execute("DELETE FROM tweets WHERE username=(?)", [user])
    c.executemany("INSERT INTO tweets(username, date_tweet, text_tweet) VALUES (?, ?, ?)", to_save)
    
    conn.commit()
    conn.close()

    # DOWNLOADING TWEETS
def get_tweets(username):
    url_for_user_id = 'https://api.twitter.com/1.1/users/show.json?screen_name=' + username
    
    # AUTHENTICATION DATA --------------------------------------------------------------------------------
    auth = OAuth1('YOUR-API-KEY', 'YOUR-API-KEY-SECRET', 'YOUR-ACCESS-TOKEN', 'YOUR-ACCESS-TOKEN-SECRET')
    # ----------------------------------------------------------------------------------------------------
    
    # authentication process
    request_id = requests.get(url_for_user_id, auth=auth)
    user_id = request_id.json().get('id')
    response_code = request_id.status_code

    if response_code == 401:
        print("Check your credentials. Remember to put your API keys in the code.")
        return

    # when entered user does not exist - end program
    if user_id is None:
        print("User", username, "does not exist")
        time.sleep(1)
        return

    # if entered user exists - try to get json response from server
    url_user_tweets = 'https://api.twitter.com/2/users/%s/tweets?tweet.fields=created_at'%user_id
    request_tweets = requests.get(url_user_tweets, auth=auth)
    json_response = request_tweets.json() 
    user_tweets = request_tweets.json().get('data')

    # if json response contains error it means user has private account -> for details uncomment code below
    if "errors" in json_response:
        #list_error = json_response.get('errors')
        #print(list_error[0].get('detail'))
        print("Sorry, you are not authorized to see the user", username)
        time.sleep(1)
        return

    if user_tweets == None:
        print("Sorry, user has no tweets.")
        return

    
    print("Downloaded", len(user_tweets), "tweets")
    
    tweets_to_db = []
    
    for tweets in user_tweets:

        # by default that's how value "created_at" looks 2022-04-25T11:32:39.000Z
        # I used datetime library to: remove T and Z letters, and then correct the timezone
        time_created = datetime.strptime(tweets.get('created_at'),"%Y-%m-%dT%H:%M:%S.%fZ").replace(
            tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S') 
            # 2022-04-25T11:32:39.000Z -> 2022-04-25 11:32:39 ->  2022-04-25 13:32:39
        tweet_text = tweets.get('text') 
        tweets_to_db.append([username, time_created, tweet_text])
        #print(time_created, "|", tweet_text) - print tweets in command line if needed
        
    save_tweets_to_db(tweets_to_db, username)
        


for username in range(1, len(usernames)):
    print("Trying to get tweets for:", usernames[username], "...")
    get_tweets(usernames[username])

