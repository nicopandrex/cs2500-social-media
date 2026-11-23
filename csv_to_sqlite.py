import sqlite3
import pandas as pd

conn = sqlite3.connect('social_media.db')

users_df = pd.read_csv('users.csv')
followers_df = pd.read_csv("followers.csv")
posts_df = pd.read_csv("posts.csv")


users_df.to_sql("users", conn, if_exists = "replace")
followers_df.to_sql("followers", conn, if_exists = "replace")
posts_df.to_sql("posts", conn, if_exists = "replace" )

conn.close()



