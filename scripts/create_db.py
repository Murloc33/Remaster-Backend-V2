import sqlite3


def main():
    connection = sqlite3.connect("../resources/remaster.db")
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sports_categories'")

    if cursor.fetchone():
        return

    cursor.execute(
        """
        CREATE TABLE doping_athletes
        (
            id                        INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name                 TEXT NULL,
            sport                     TEXT NULL,
            birth_date                TEXT NULL,
            violation_description     TEXT NULL,
            disqualification_duration TEXT NULL,
            disqualification_start    TEXT NULL,
            disqualification_end      TEXT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE sports_categories
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO sports_categories (name)
        VALUES ('кандидат в мастера спорта'),
               ('первый спортивный разряд')
        """
    )

    cursor.execute(
        """
        CREATE TABLE sports
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO sports (name)
        VALUES ('Легкая атлетика'),
               ('Спортивное программирование'),
               ('Компьютерный спорт')
        """
    )

    cursor.execute(
        """
        CREATE TABLE documents
        (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            title              TEXT    NOT NULL,
            sports_category_id INTEGER NOT NULL,
            created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sports_category_id) REFERENCES sports_categories (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE document_athletes
        (
            id                         INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id                INTEGER NOT NULL,
            full_name                  TEXT    NOT NULL,
            birth_date                 TEXT    NOT NULL,
            sport_id                   INTEGER NOT NULL,
            municipality               TEXT    NOT NULL,
            organization               TEXT    NOT NULL,
            is_sports_category_granted BOOLEAN NOT NULL,
            is_doping_check_passed     BOOLEAN NOT NULL,
            created_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents (id),
            FOREIGN KEY (sport_id) REFERENCES sports (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE sports_category_verifications
        (
            id                         INTEGER PRIMARY KEY AUTOINCREMENT,
            document_athlete_id        INTEGER NOT NULL,
            json_data                  TEXT    NOT NULL,
            is_sports_category_granted BOOLEAN NOT NULL,
            created_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_athlete_id) REFERENCES document_athletes (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE databases
        (
            slug  TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            date  TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO databases
        VALUES ('orders', 'Шаблон приказа', ''),
               ('doping-athletes', '(База) Русадо', ''),
               ('athletics', '(База) Легкая атлетика', ''),
               ('programming', '(База) Спортивное программирование', ''),
               ('computer-sport', '(База) Компьютерный спорт', '')
        """
    )

    connection.commit()
    print("База данных успешно инициализирована")


if __name__ == "__main__":
    main()
