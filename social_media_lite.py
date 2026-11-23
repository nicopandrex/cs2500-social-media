import sqlite3
import pwinput



class Login:
    conn = sqlite3.connect("social_media.db")

    
    
    
    def login_screen(self):
        success = False
        print("Welcome to Social Media Lite")
        while not success:
            user_name = input("Username: ")
            if self.try_user(user_name):
                password = pwinput.pwinput(prompt='Password: ') 
                if self.try_pass(user_name, password):
                    print("Successful Login")
                    success = True
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
    
    

login = Login()

login.login_screen()
