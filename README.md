# twitter-sql
Simple command line program for downloading tweets from selected users.

Before using program be sure to add your API credentials from Twitter Developer site in the code.

# Usage
python **main.py [usernames]**

Program takes usernames as arguments. You can pass multiple usernames. 

For every username maximum of **10 latest tweets** will be downloaded.

# Database
After downloading tweets are saved in "tweets_database.db" file. 
Every tweet object has 3 values: username, creation date and content. 
Tweets are stored in "tweets" table. 

For every user only 10 tweets can be saved into database.
With every download, new tweets will replace old ones for each user.



