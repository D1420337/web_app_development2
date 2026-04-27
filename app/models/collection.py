from app.models.db import get_db_connection
import sqlite3

class Collection:
    @staticmethod
    def add(user_id, recipe_id):
        """新增收藏"""
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO collection (user_id, recipe_id) VALUES (?, ?)",
                (user_id, recipe_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # 已經收藏過了
        finally:
            conn.close()

    @staticmethod
    def remove(user_id, recipe_id):
        """取消收藏"""
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM collection WHERE user_id = ? AND recipe_id = ?",
            (user_id, recipe_id)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_user_collections(user_id):
        """取得使用者的所有收藏清單"""
        conn = get_db_connection()
        recipes = conn.execute(
            """
            SELECT r.*, u.username as author_name, c.created_at as collected_at
            FROM collection c
            JOIN recipe r ON c.recipe_id = r.id
            JOIN user u ON r.user_id = u.id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
            """,
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in recipes]
    
    @staticmethod
    def is_collected(user_id, recipe_id):
        """檢查特定使用者是否已經收藏特定食譜"""
        conn = get_db_connection()
        result = conn.execute(
            "SELECT 1 FROM collection WHERE user_id = ? AND recipe_id = ?",
            (user_id, recipe_id)
        ).fetchone()
        conn.close()
        return bool(result)
