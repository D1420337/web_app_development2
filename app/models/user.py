from app.models.db import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash, role='user'):
        """建立新使用者"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO user (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Username already exists
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得使用者"""
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        """根據使用者名稱取得使用者"""
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None
