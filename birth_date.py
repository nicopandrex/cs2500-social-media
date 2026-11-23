import sqlite3

birth_dates = ["10/18/1999", "8/19/1998", "9/29/2001", "11/26/1995","10/22/2002", "12/22/1999", "10/5/2000", "1/3/2003",]

conn = sqlite3.connect("social_media.db")

# conn.execute("ALTER TABLE users ADD birth_date TEXT")

users = conn.execute(
    "SELECT user_id FROM users ORDER BY user_id"
).fetchall()



for i in range(len(users)):
    user_id = users[i][0]
    birth_date = birth_dates[i]

    conn.execute(
        "UPDATE users SET birth_date = ? WHERE user_id = ?",
        (birth_date, user_id),
    )

conn.commit()
conn.close()

