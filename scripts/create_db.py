import sqlite3
import os
from datetime import datetime

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect("../resources/remaster.db")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def init_db(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sports_categories'")
        if self.cursor.fetchone():
            return

        try:
            self.cursor.execute("""
                CREATE TABLE doping_athletes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NULL,
                    sport TEXT NULL,
                    birth_date TEXT NULL,
                    violation_description TEXT NULL,
                    disqualification_duration TEXT NULL,
                    disqualification_start TEXT NULL,
                    disqualification_end TEXT NULL
                )
            """)

            self.cursor.execute("""
                CREATE TABLE sports_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """)

            self.cursor.execute("""
                INSERT INTO sports_categories (name)
                VALUES ('КМС'), ('1 спортивный')
            """)

            self.cursor.execute("""
                CREATE TABLE sports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)

            self.cursor.execute("""
                INSERT INTO sports (name)
                VALUES ('Легкая атлетика'), 
                       ('Спортивное программирование'), 
                       ('Компьютерный спорт')
            """)

            self.cursor.execute("""
                CREATE TABLE documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    sports_category_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sports_category_id) REFERENCES sports_categories (id)
                )
            """)

            self.cursor.execute("""
                CREATE TABLE document_athletes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    full_name TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    sport_id INTEGER NOT NULL,
                    municipality TEXT NOT NULL,
                    organization TEXT NOT NULL,
                    is_sports_category_granted BOOLEAN NOT NULL,
                    is_doping_check_passed BOOLEAN NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id),
                    FOREIGN KEY (sport_id) REFERENCES sports (id)
                )
            """)

            self.cursor.execute("""
                CREATE TABLE sports_category_verifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_athlete_id INTEGER NOT NULL,
                    json_data TEXT NOT NULL,
                    is_sports_category_granted BOOLEAN NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_athlete_id) REFERENCES document_athletes(id)
                )
            """)

            self.cursor.execute("""
                CREATE TABLE databases (
                    slug TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """)

            self.cursor.execute("""
                INSERT INTO databases VALUES 
                ('order', 'Шаблон приказа', ''),
                ('doping-athletes', '(База) Русадо', ''),
                ('athletics', '(База) Легкая атлетика', ''),
                ('programming', '(База) Спортивное программирование', ''),
                ('computer-sport', '(База) Компьютерный спорт', '')
            """)

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Ошибка при создании базы данных: {e}")
            self.conn.rollback()

if __name__ == "__main__":
    db = DBManager()
    db.init_db()
    print("База данных успешно инициализирована")