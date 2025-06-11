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
        VALUES ('КМС'),
               ('1 спортивный')
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

    cursor.execute(
        """
        CREATE TABLE sports_programming_competition_statuses
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO sports_programming_competition_statuses (name)
        VALUES ('Чемпионат мира'),
               ('Чемпионат Европы'),
               ('Первенство мира'),
               ('Всемирные студенческие игры'),
               ('Первенство Европы'),
               ('Другие международные спортивные соревнования, включенные в ЕКП'),
               ('Чемпионат России'),
               ('Кубок России (при двух и более этапах – финал)'),
               ('Первенство России'),
               ('Другие всероссийские спортивные соревнования, включенные в ЕКП'),
               ('Чемпионат федерального округа, двух и более федеральных округов'),
               ('Первенство федерального округа, двух и более федеральных округов'),
               ('Другие межрегиональные спортивные соревнования, включенные в ЕКП'),
               ('Чемпионат субъекта Российской Федерации'),
               ('Кубок субъекта Российской Федерации (при двух и более этапах – финал)')
        """
    )


    cursor.execute(
        """
        CREATE TABLE sports_programming
        (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,

            sports_category_id  INTEGER NOT NULL,
            competition_status_id INTEGER NOT NULL,

            place_from            INTEGER NOT NULL,
            place_to              INTEGER NOT NULL,

            age_from              INTEGER NOT NULL,
            age_to                INTEGER,

            FOREIGN KEY (sports_category_id) REFERENCES sports_categories (id),
            FOREIGN KEY (competition_status_id) REFERENCES sports_programming_competition_statuses (id)
        )
        """
    )

    # cursor.execute(
    #     """
    #     CREATE TABLE computer_sport_type
    #     (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL UNIQUE
    #     )
    #     """
    # )
    #
    # cursor.execute(
    #     """
    #     INSERT INTO computer_sport_type (name)
    #     VALUES ('Боевая арена, соревновательные головоломки, стратегия в реальном времени, файтинг, тактический трехмерный бой'),
    #            ('Спортивный симулятор, технический симулятор')
    #     """
    # )
    #
    # cursor.execute(
    #     """
    #     CREATE TABLE competition_filters_computer_sport
    #     (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         sports_categories_id INTEGER NOT NULL,
    #         place_from INTEGER NOT NULL,
    #         place_to  INTEGER NOT NULL,
    #         competition_status_id INTEGER NOT NULL,
    #         age_from  INTEGER NOT NULL,
    #         age_to  INTEGER NOT NULL,
    #         match_win INTEGER NOT NULL,
    #         computer_sport_type_id INTEGER NOT NULL,
    #         FOREIGN KEY (sports_categories_id) REFERENCES sports_categories (id),
    #         FOREIGN KEY (competition_status_id) REFERENCES competition_status (id),
    #         FOREIGN KEY (computer_sport_type_id) REFERENCES computer_sport_type (id)
    #     )
    #     """
    # )

    connection.commit()
    print("База данных успешно инициализирована")


if __name__ == "__main__":
    main()
