import sqlite3
import pwinput



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
    



def menu(username):
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
            case "1": pass   
            case "2": pass  
            case "3": pass   
            case "4": pass   
            case "5": pass   
            case "6":
                return
            case _:
                print("\nInvalid Selection")


login = Login()

while True:
    username = login.login_screen()
    menu(username)
    print("Logged out.\n")

