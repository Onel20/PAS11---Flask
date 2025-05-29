import mysql.connector

class CommentModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            database="ensiklopedia",
            user="root",
            password=""
        )
        self.conn.autocommit = False
        self.cursor = self.conn.cursor(dictionary=True)

    def get_comments_by_article(self, article_id):
        q = """
        SELECT c.id, c.comment_text, c.user_id, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.article_id = %s
        ORDER BY c.id DESC
        """
        self.cursor.execute(q, (article_id,))
        return self.cursor.fetchall()

    def insert_comment(self, article_id, user_id, comment_text):
        try:
            q = "INSERT INTO comments (article_id, user_id, comment_text) VALUES (%s, %s, %s)"
            self.cursor.execute(q, (article_id, user_id, comment_text))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def update_comment(self, comment_id, comment_text):
        try:
            self.cursor.execute(
                "UPDATE comments SET comment_text = %s WHERE id = %s",
                (comment_text, comment_id)
            )
            self.conn.commit()
        except:
            self.conn.rollback()
            raise

    def get_by_id(self, comment_id):
        q = """
        SELECT c.*, u.username 
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.id = %s
        """
        self.cursor.execute(q, (comment_id,))
        return self.cursor.fetchone()

    def delete_comment(self, comment_id):
        try:
            self.cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
            self.conn.commit()
        except:
            self.conn.rollback()
            raise

    def close(self):
        self.cursor.close()
        self.conn.close()
