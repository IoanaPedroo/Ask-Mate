import data_connection
from datetime import datetime

@data_connection.connection_handler
def add_user(cursor, result):
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        """
            INSERT INTO users (username, password, registration, reputation)
            VALUES (%(username)s, %(password)s, %(registration)s, %(reputation)s);
        """,
        {
            "username": result["email"],
            "password": result["password"],
            "registration": date,
            "reputation": 0,
        },
    )


@data_connection.connection_handler
def select_users(cursor):
    cursor.execute(
        """
            SELECT * FROM users;
        """
    )
    return cursor.fetchall()

@data_connection.connection_handler
def count_q_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT COUNT(user_id) AS questions FROM question WHERE user_id =%(user_id)s;
        """,
        {"user_id": user_id},
    )
    return cursor.fetchone()

@data_connection.connection_handler
def count_a_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT COUNT(user_id) AS answers FROM answer WHERE user_id =%(user_id)s;
        """,
        {"user_id": user_id},
    )
    return cursor.fetchone()


@data_connection.connection_handler
def count_c_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT COUNT(user_id) AS comments FROM comment WHERE user_id =%(user_id)s;
        """,
        {"user_id": user_id},
    )
    return cursor.fetchone()

@data_connection.connection_handler
def get_q_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM question WHERE user_id=%(user_id)s;
        """,
        {"user_id": user_id},
    )
    return cursor.fetchall()

@data_connection.connection_handler
def get_a_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM answer WHERE user_id=%(user_id)s;
        """,
        {"user_id": user_id},
    )
    return cursor.fetchall()

@data_connection.connection_handler
def get_c_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM comment WHERE user_id=%(user_id)s;
        """,
        {"user_id": user_id},
    )
    return cursor.fetchall()

@data_connection.connection_handler
def change_reputation(cursor, user_id, value):
    cursor.execute(
        """
        UPDATE users
        SET  reputation = reputation + %(value)s
        WHERE id=%(user_id)s
        """,
        {"user_id": user_id, "value": value},
    )

@data_connection.connection_handler
def select_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM users WHERE id=%(user_id)s;
        """,
        {"user_id": user_id},
    )
    return cursor.fetchone()

@data_connection.connection_handler
def get_user(cursor, question_id):
    cursor.execute("""
    SELECT user_id FROM question WHERE id = %(question_id)s;""",
                   {"question_id": question_id},
                   )
    return cursor.fetchone()


@data_connection.connection_handler
def get_user_2(cursor, answer_id):
    cursor.execute("""
    SELECT user_id FROM answer WHERE id = %(answer_id)s;""",
                   {
                       "answer_id": answer_id
                   })
    return cursor.fetchone()
