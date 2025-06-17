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
            doping_data                ANY NULL,
            result_data                ANY NULL,
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

            sports_category_id    INTEGER NOT NULL,
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

    cursor.execute(
        """
        CREATE TABLE computer_sport_competition_statuses
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO computer_sport_competition_statuses (name)
        VALUES ('Чемпионат мира'),
               ('Чемпионат Европы'),
               ('Кубок  Европы (при двух и более этапах  –  финал)'),
               ('Другие международные спортивные соревнования, включенные в ЕКП'),
               ('Чемпионат России'),
               ('Кубок России (при двух и более этапах – финал)'),
               ('Первенство России'),
               ('Другие всероссийские спортивные соревнования, включенные в ЕКП'),
               ('Выполняется получение данных. Подождите несколько секунд, а затем еще раз попробуйте вырезать или скопировать'),
               ('Чемпионат федерального округа, двух и более федеральных округов, чемпионаты г. Москвы, г. Санкт-Петербурга'),
               ('Другие межрегиональные спортивные соревнования, включенные в ЕКП'),
               ('Чемпионат субъекта Российской Федерации (кроме г. Москвы и г. Санкт-Петербурга)'),
               ('Кубок субъекта Российской Федерации (при двух и более этапах – финал)'),
               ('Другие официальные спортивные соревнования субъекта Российской Федерации')
        """
    )

    cursor.execute(
        """
        CREATE TABLE computer_sport_discipline
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO computer_sport_discipline (name)
        VALUES ('Боевая арена'),
               ('Cоревновательные головоломки'),
               ('Cтратегия в реальном времени'),
               ('Файтинг'),
               ('Тактический трехмерный бой'),
               ('Спортивный симулятор'),
               ('Технический симулятор')
        """
    )

    cursor.execute(
        """
        CREATE TABLE computer_sport
        (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_status_id INTEGER NOT NULL,
            discipline_id         INTEGER NOT NULL,
            sports_category_id    INTEGER NOT NULL,

            place_from            INTEGER NOT NULL,
            place_to              INTEGER NOT NULL,

            win_match             INTEGER NOT NULL,

            is_internally_subject BOOLEAN NOT NULL,
            subject_from          INTEGER NULL,
            subject_to            INTEGER NULL,

            FOREIGN KEY (competition_status_id) REFERENCES computer_sport_competition_statuses (id),
            FOREIGN KEY (discipline_id) REFERENCES computer_sport_discipline (id),
            FOREIGN KEY (sports_category_id) REFERENCES sports_categories (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE sex
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO sex (name)
        VALUES ('М'),
               ('Ж'),
               ('Оба')
        """
    )

    cursor.execute(
        """
        CREATE TABLE athletics_discipline_contents
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE athletics_based_on_place_disciplines
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE system_counting
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO system_counting (name)
        VALUES ('секунды'),
               ('минуты')
        """
    )

    cursor.execute(
        """
        CREATE TABLE athletics_discipline
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            sex_id INTEGER NOT NULL,
            name TEXT NOT NULL UNIQUE,
            system_counting_id INTEGER NOT NULL,
            
            FOREIGN KEY (sex_id) REFERENCES sex (id),
            FOREIGN KEY (system_counting_id) REFERENCES system_counting (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE athletics_adapter_disciplines
        (
            based_on_place_discipline_id INTEGER NOT NULL,
            discipline_id INTEGER NOT NULL,
            FOREIGN KEY (based_on_place_discipline_id) REFERENCES athletics_based_on_place_disciplines (id),
            FOREIGN KEY (discipline_id) REFERENCES athletics_discipline (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE athletics_competition_statuses
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO athletics_competition_statuses (name)
        VALUES ('')
        """
    )

    cursor.execute(
        """
        CREATE TABLE athletics_based_on_place_records
        (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_status_id INTEGER NOT NULL,
            based_on_place_discipline_id INTEGER NOT NULL,
            sports_category_id INTEGER NOT NULL,
            
            age_from INTEGER NOT NULL,
            age_to INTEGER NULL,
            
            place_from  INTEGER NOT NULL,
            place_to  INTEGER NOT NULL,
            
            min_count_participants INTEGER NOT NULL,
            
            FOREIGN KEY (competition_status_id) REFERENCES athletics_competition_statuses (id),
            FOREIGN KEY (based_on_place_discipline_id) REFERENCES athletics_based_on_place_disciplines (id),
            FOREIGN KEY (sports_category_id) REFERENCES sports_categories (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE athletics_based_on_result_records
        (
            id                           INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_status_id        INTEGER NOT NULL,
            discipline_id                INTEGER NOT NULL,
            discipline_content_id        INTEGER NOT NULL,
            sports_category_id           INTEGER NOT NULL,
            sex_id                       INTEGER NOT NULL,

            age_from                     INTEGER NOT NULL,
            age_to                       INTEGER NULL,
    
            min_result                   INTEGER NOT NULL,
            min_count_participants       INTEGER NOT NULL,

            FOREIGN KEY (competition_status_id) REFERENCES athletics_competition_statuses (id),
            FOREIGN KEY (discipline_content_id) REFERENCES athletics_discipline_contents (id),
            FOREIGN KEY (discipline_id) REFERENCES athletics_discipline (id),
            FOREIGN KEY (sports_category_id) REFERENCES sports_categories (id),
            FOREIGN KEY (sex_id) REFERENCES  sex (id)
        )
        """
    )

    connection.commit()
    print("База данных успешно инициализирована")


if __name__ == "__main__":
    main()
