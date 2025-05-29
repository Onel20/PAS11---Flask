import mysql.connector

class ArticleModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            database="ensiklopedia",
            user="root",
            password=""
        )
        self.conn.autocommit = False
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all_articles(self):
        q = """
        SELECT a.*, u.username FROM articles a
        JOIN users u ON a.author_id = u.id
        """
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def get_article_by_id(self, id):
        q = """
        SELECT a.*, u.username FROM articles a
        JOIN users u ON a.author_id = u.id
        WHERE a.id = %s
        """
        self.cursor.execute(q, (id,))
        return self.cursor.fetchone()

    def insert_article(self, title, content, subject, author_id):
        try:
            q = "INSERT INTO articles (title, content, subject, author_id) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(q, (title, content, subject, author_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def update_article(self, article_id, title, content, subject):
        try:
            self.cursor.execute(
                "UPDATE articles SET title = %s, content = %s, subject = %s WHERE id = %s",
                (title, content, subject, article_id)
            )
            self.conn.commit()
        except:
            self.conn.rollback()
            raise

    def delete_article(self, article_id):
        try:
            # First delete all comments associated with this article
            self.cursor.execute("DELETE FROM comments WHERE article_id = %s", (article_id,))
            # Then delete the article
            self.cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
            self.conn.commit()
        except:
            self.conn.rollback()
            raise

    def close(self):
        self.cursor.close()
        self.conn.close()
