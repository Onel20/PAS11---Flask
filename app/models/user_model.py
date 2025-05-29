import mysql.connector

class UserModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            database="ensiklopedia",
            user="root",
            password=""
        )
        self.conn.autocommit = False
        self.cursor = self.conn.cursor(dictionary=True)

    def get_user_by_id(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def get_user_by_username(self, username):
        query = "SELECT id, username, password FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def insert_user(self, username, password):
        try:
            q = "INSERT INTO users (username, password) VALUES (%s, %s)"
            self.cursor.execute(q, (username, password))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        
    def update_password(self, user_id, new_password):
        try:
            self.cursor.execute(
                "UPDATE users SET password = %s WHERE id = %s",
                (new_password, user_id)
            )
            self.conn.commit()
        except:
            self.conn.rollback()
            raise

    def close(self):
        self.cursor.close()
        self.conn.close()
