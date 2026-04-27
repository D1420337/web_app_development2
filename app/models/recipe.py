from app.models.db import get_db_connection

class Recipe:
    @staticmethod
    def create(user_id, title, description, ingredients, instructions):
        """新增食譜"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipe (user_id, title, description, ingredients, instructions)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, title, description, ingredients, instructions)
        )
        conn.commit()
        recipe_id = cursor.lastrowid
        conn.close()
        return recipe_id

    @staticmethod
    def get_all():
        """取得所有食譜"""
        conn = get_db_connection()
        recipes = conn.execute(
            """
            SELECT r.*, u.username as author_name 
            FROM recipe r 
            JOIN user u ON r.user_id = u.id 
            ORDER BY r.created_at DESC
            """
        ).fetchall()
        conn.close()
        return [dict(row) for row in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        """根據 ID 取得食譜"""
        conn = get_db_connection()
        recipe = conn.execute(
            """
            SELECT r.*, u.username as author_name 
            FROM recipe r 
            JOIN user u ON r.user_id = u.id 
            WHERE r.id = ?
            """,
            (recipe_id,)
        ).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def search(keyword):
        """搜尋食譜"""
        conn = get_db_connection()
        search_query = f"%{keyword}%"
        recipes = conn.execute(
            """
            SELECT r.*, u.username as author_name 
            FROM recipe r 
            JOIN user u ON r.user_id = u.id 
            WHERE r.title LIKE ? OR r.ingredients LIKE ?
            ORDER BY r.created_at DESC
            """,
            (search_query, search_query)
        ).fetchall()
        conn.close()
        return [dict(row) for row in recipes]

    @staticmethod
    def update(recipe_id, title, description, ingredients, instructions):
        """更新食譜"""
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE recipe 
            SET title = ?, description = ?, ingredients = ?, instructions = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, description, ingredients, instructions, recipe_id)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(recipe_id):
        """刪除食譜"""
        conn = get_db_connection()
        conn.execute("DELETE FROM recipe WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()
        return True
