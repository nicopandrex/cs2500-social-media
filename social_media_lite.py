import sqlite3
import pwinput
from datetime import datetime



class Login:
    conn = sqlite3.connect("social_media.db")

    
    
    
    def login_screen(self):
        print("Welcome to Social Media Lite")
        while True:
            user_name = input("Username: ")
            if self.try_user(user_name):
                password = pwinput.pwinput(prompt='Password: ')
                if self.try_pass(user_name, password):
                    print("Successful Login")
                    return user_name
                else:
                    print("Access Denied")
            else:
                print("User not found")

    def try_user(self,user_name):
        query = "SELECT username FROM users WHERE username = ?"
        
        result = self.conn.execute(query, (user_name,)).fetchone()

        return result is not None
    
    def try_pass(self,user_name,pword):
        query = "SELECT username, password FROM users WHERE username = ? AND password = ?"
        
        result = self.conn.execute(query, (user_name, pword)).fetchone()

        return result is not None
    



def view_info(user_name):
    query = "SELECT * FROM users WHERE username = ?"
    conn = sqlite3.connect("social_media.db")
    
    user_info = conn.execute(query,(user_name,)).fetchall()
    
    user_id = user_info[0][1]
    email = user_info[0][2]
    username = user_info[0][3]
    password = user_info[0][4]
    account_created = user_info[0][5]
    first_name = user_info[0][6]
    last_name = user_info[0][7]
    birth_date = user_info[0][8]
    
    info_printable = f"""
_________________INFO___________________
ID: {user_id}
Email: {email}
Username: {username}
Account Creation Date: {account_created}
First Name: {first_name}
Last Name: {last_name}
Birth Date: {birth_date}
"""
    print(info_printable)
    
    
def update_info(user_name):
    conn = sqlite3.connect("social_media.db")

    def save(column, value):
        conn.execute(f"UPDATE users SET {column} = ? WHERE username = ?", (value, user_name))
        conn.commit()

    while True:
        print("""
_________________UPDATE INFO____________
1. Username
2. Password
3. Email
4. First Name
5. Last Name
6. Birth Date
7. Back to Menu
""")
        choice = input("Input Selection (1-7): ").strip()

        match choice:
            case "1":
                new_name = input("New username: ").strip()
                if not new_name:
                    print("Username cannot be empty.")
                elif new_name == user_name:
                    print("That is already your username.")
                elif conn.execute("SELECT 1 FROM users WHERE username = ?", (new_name,)).fetchone():
                    print("That username is already taken.")
                else:
                    save("username", new_name)
                    user_name = new_name
                    print("Username updated.")
            case "2":
                current = pwinput.pwinput(prompt="Current password: ")
                if not conn.execute("SELECT 1 FROM users WHERE username = ? AND password = ?",
                                    (user_name, current)).fetchone():
                    print("Incorrect password.")
                    continue
                new_pass = pwinput.pwinput(prompt="New password: ")
                if not new_pass:
                    print("Password cannot be empty.")
                elif new_pass != pwinput.pwinput(prompt="Confirm new password: "):
                    print("Passwords do not match.")
                else:
                    save("password", new_pass)
                    print("Password updated.")
            case "3":
                email = input("New email: ").strip()
                if "@" not in email or "." not in email:
                    print("Please enter a valid email.")
                else:
                    save("email_id", email)
                    print("Email updated.")
            case "4":
                first = input("New first name: ").strip()
                if first:
                    save("first_name", first)
                    print("First name updated.")
                else:
                    print("First name cannot be empty.")
            case "5":
                last = input("New last name: ").strip()
                if last:
                    save("last_name", last)
                    print("Last name updated.")
                else:
                    print("Last name cannot be empty.")
            case "6":
                raw = input("New birth date (MM/DD/YYYY): ").strip()
                try:
                    d = datetime.strptime(raw, "%m/%d/%Y")
                except ValueError:
                    print("Invalid date. Use MM/DD/YYYY.")
                    continue
                if d > datetime.now():
                    print("Birth date cannot be in the future.")
                else:
                    save("birth_date", f"{d.month}/{d.day}/{d.year}")
                    print("Birth date updated.")
            case "7":
                conn.close()
                return user_name
            case _:
                print("\nInvalid Selection")
                
                
                
def view_posts(user_name):
    
    conn = sqlite3.connect("social_media.db")
    
    user_id_query = "SELECT user_id FROM users WHERE username = ?"
    
    user_id = conn.execute(user_id_query,(user_name,)).fetchone()[0]

    posts_query = "SELECT post, posted_date FROM posts WHERE user_id = ?"

    posts = conn.execute(posts_query, (user_id,)).fetchall()
    conn.close()

    print("\n______________YOUR POSTS____________")
    if not posts:
        print("You have no posts yet.")
    for post in posts:
        print(f"\nDate: {post[1]}\nPost: {post[0]}")
        
    
def publish_post(user_name):
    conn = sqlite3.connect("social_media.db")
    user_id_query = "SELECT user_id FROM users WHERE username = ?"
    user_id = conn.execute(user_id_query,(user_name,)).fetchone()[0]
    
    create_post_query = "INSERT INTO posts (user_id, post, posted_date) VALUES (?,?,?)"
    
    post_text = input("Write your post (leave blank to cancel): ").strip()

    if not post_text:
        print("Post cancelled.")
        conn.close()
        return

    now = datetime.now()
    
    posted_date = f"{now.month}/{now.day}/{now.year}"

    conn.execute(create_post_query, (user_id, post_text, posted_date))
    conn.commit()
    conn.close()
    print("Post published!")


def view_follows(user_name):
    conn = sqlite3.connect("social_media.db")
    user_id = conn.execute("SELECT user_id FROM users WHERE username = ?",
                           (user_name,)).fetchone()[0]

    
    following = conn.execute(
        """SELECT u.username, u.first_name, u.last_name
           FROM followers f JOIN users u ON u.user_id = f.follow_id
           WHERE f.user_id = ?""", (user_id,)).fetchall()

    followers = conn.execute(
        """SELECT u.username, u.first_name, u.last_name
           FROM followers f JOIN users u ON u.user_id = f.user_id
           WHERE f.follow_id = ?""", (user_id,)).fetchall()
    conn.close()

    print("\n______________FOLLOWING____________")
    if not following:
        print("You are not following anyone yet.")
    for username, first, last in following:
        print(f"{username} ({first} {last})")

    print("\n______________FOLLOWERS____________")
    if not followers:
        print("You have no followers yet.")
    for username, first, last in followers:
        print(f"{username} ({first} {last})")



def menu(user_name):
    options = """
_________________MENU___________________
1. View Info
2. Update Info
3. View Posts
4. Publish Post
5. View Followers and Following
6. Log Out
"""
    while True:
        print(options)
        selection = input("Input Selection (1-6): ").strip()
        match selection:
            case "1":
                view_info(user_name)
                input("Press Enter to return to the menu...")
            case "2":
                user_name = update_info(user_name)
            case "3": 
                view_posts(user_name)   
                input("Press Enter to return to the menu...")
            case "4":
                publish_post(user_name)
                input("Press Enter to return to the menu...")
            case "5":
                view_follows(user_name)
                input("Press Enter to return to the menu...")
            case "6":
                return
            case _:
                print("\nInvalid Selection")


#run loop
login = Login()

while True:
    user_name = login.login_screen()
    menu(user_name)
    print("Logged out.\n")

