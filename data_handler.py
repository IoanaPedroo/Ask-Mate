import data_connection
from datetime import datetime


@data_connection.connection_handler
def get_last_five_question(cursor):
    cursor.execute(
        """
            SELECT * FROM question
            ORDER BY submission_time DESC
            LIMIT 5;
        """
    )
    return cursor.fetchall()


@data_connection.connection_handler
def sort_q(cursor, order_by, order_direction):
    cursor.execute(
        f"""
            SELECT * FROM question 
            ORDER BY {order_by} {order_direction};
        """
    )
    return cursor.fetchall()


@data_connection.connection_handler
def get_questions(cursor):
    cursor.execute("SELECT * FROM question")
    return cursor.fetchall()


@data_connection.connection_handler
def get_answers(cursor, question_id):
    cursor.execute(
        """
            SELECT * FROM answer
            WHERE question_id=%(question_id)s
            ORDER BY id;
        """,
        {"question_id": question_id},
    )
    return cursor.fetchall()


@data_connection.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute(
        "SELECT * FROM answer where id = %(answer_id)s;",
        {"answer_id": answer_id},
    )
    return cursor.fetchone()


@data_connection.connection_handler
def get_question(cursor, question_id):
    cursor.execute(
        "SELECT * FROM question where id = %(question_id)s;",
        {"question_id": question_id},
    )
    return cursor.fetchone()


@data_connection.connection_handler
def add_new_data_to_table(cursor, result, content):

    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    if content == "question":
        cursor.execute(
            """
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s, %(user_id)s);
            """,
            {
                "submission_time": date,
                "view_number": result["view_number"],
                "vote_number": result["vote_number"],
                "title": result["title"],
                "message": result["message"],
                "image": result["image"],
                "user_id": result['user_id']
            },
        )

    elif content == "answer":
        cursor.execute(
            """
                INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id, acceptance)
                VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_id)s, %(acceptance_answers)s);
            """,
            {
                "submission_time": date,
                "vote_number": result["vote_number"],
                "question_id": result["question_id"],
                "message": result["message"],
                "image": result["image"],
                "user_id": result['user_id'],
                "acceptance_answers": False
            },
        )

    elif content == "comment":
        cursor.execute(
            """
                INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
                VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s);
            """,
            {
                "question_id": result["question_id"],
                "answer_id": result["answer_id"],
                "message": result["message"],
                "submission_time": date,
                "edited_count": result["edited_count"],
                "user_id": result['user_id']
            },
        )


@data_connection.connection_handler
def delete_function(cursor, question_id):
    cursor.execute(
        """
            DELETE FROM comment
            WHERE question_id = %(question_id)s;

            DELETE FROM answer
            WHERE question_id = %(question_id)s;

            DELETE FROM question_tag
            WHERE question_id = %(question_id)s;

            DELETE FROM question
            WHERE id = %(question_id)s;
       """,
        {"question_id": question_id},
    )


@data_connection.connection_handler
def delete_answer(cursor, question_id, answer_id):
    cursor.execute(
        """
            DELETE FROM comment
            WHERE question_id = %(question_id)s AND answer_id = %(answer_id)s;

            DELETE FROM answer
            WHERE id = %(answer_id)s;
        """,
        {"question_id": question_id, "answer_id": answer_id},
    )


@data_connection.connection_handler
def vote_question(cursor, question_id, count):
    vote = 1 if count == "up" else -1

    cursor.execute(
        """
            UPDATE question SET vote_number = vote_number + %(vote)s
            WHERE id = %(question_id)s;
        """,
        {
            "question_id": question_id,
            "vote": vote,
        },
    )


@data_connection.connection_handler
def vote_answer(cursor, answer_id, count):
    vote = 1 if count == "up" else -1
    cursor.execute(
        """
            UPDATE answer
            SET vote_number = vote_number + %(vote)s
            WHERE id = %(answer_id)s;
        """,
        {
            "answer_id": answer_id,
            "vote": vote,
        },
    )


@data_connection.connection_handler
def edit_question(cursor, question_id, edited_title, edited_message):
    cursor.execute(
        """
            UPDATE question
            SET title = %(edited_title)s, message = %(edited_message)s
            WHERE id = %(question_id)s;
        """,
        {
            "question_id": question_id,
            "edited_title": edited_title,
            "edited_message": edited_message,
        },
    )


@data_connection.connection_handler
def get_comments_for_question(cursor, question_id):
    cursor.execute(
        "SELECT * FROM comment WHERE question_id = %(question_id)s;",
        {"question_id": question_id},
    )
    return cursor.fetchall()


@data_connection.connection_handler
def get_comments_for_answer(cursor, answer_id):
    cursor.execute(
        "SELECT * FROM comment WHERE answer_id = %(answer_id)s;",
        {"answer_id": answer_id},
    )
    return cursor.fetchall()



@data_connection.connection_handler
def edit_comments(cursor, comment, edited_comment):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute(
        """
            UPDATE comment
            SET submission_time = %(submission_time)s, message = %(message)s, edited_count = edited_count + 1
            WHERE id = %(comment_id)s;
        """,
        {
            "comment_id": comment['id'],
            "message": message,
            "submission_time": dt,
        },
    )


@data_connection.connection_handler
def edit_question_answer(cursor, result):
    cursor.execute(
        """
            UPDATE answer
            SET message = %(message)s
            WHERE id = %(answer_id)s AND question_id = %(question_id)s;
        """,
        result,
    )

@data_connection.connection_handler
def edit_comments(cursor ,result):
    print(result)
    cursor.execute(
        """
            UPDATE comment
            SET message =  %(message)s,
            WHERE id = %(id)s ;
        """,
        {'message':result['message'],
        'id':result['id']}
    )


@data_connection.connection_handler
def increase_view_numbers(cursor, question_id):
    cursor.execute(
        """
            UPDATE question
            SET view_number = view_number + 1
            WHERE id = %(question_id)s;
        """,
        {"question_id": question_id},
    )


@data_connection.connection_handler
def get_query(cursor, search):
    cursor.execute(
        """
            SELECT * FROM question
            WHERE title iLIKE %(search)s or message iLIKE %(search)s;
        """,
        {"search": "%" + search + "%"},
    )
    return cursor.fetchall()


@data_connection.connection_handler
def checkout_data(cursor, email):
    cursor.execute(
        """
        SELECT id, username as email, password, registration FROM users WHERE username = %(username)s;
        """,
        {
            "username": email,
        },
    )
    return cursor.fetchone()


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
            "reputation": 0

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
        {
            "user_id": user_id
        }
    )
    return cursor.fetchone()



@data_connection.connection_handler
def count_a_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT COUNT(user_id) AS answers FROM answer WHERE user_id =%(user_id)s;
        """,
        {
            "user_id": user_id
        }
    )
    return cursor.fetchone()



@data_connection.connection_handler
def count_c_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT COUNT(user_id) AS comments FROM comment WHERE user_id =%(user_id)s;
        """,
        {
            "user_id": user_id
        }
    )
    return cursor.fetchone()



@data_connection.connection_handler
def get_q_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM question WHERE user_id=%(user_id)s;
        """,
        {
            "user_id": user_id
        }
    )
    return cursor.fetchall()


@data_connection.connection_handler
def get_a_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM answer WHERE user_id=%(user_id)s;
        """,
        {
            "user_id": user_id
        }
    )
    return cursor.fetchall()


@data_connection.connection_handler
def get_c_by_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM comment WHERE user_id=%(user_id)s;
        """,
        {
            "user_id": user_id
        }
    )
    return cursor.fetchall()


@data_connection.connection_handler
def accept_answer(cursor, user_id):
    cursor.execute(
        """
        UPDATE answer
        SET acceptance = (CASE WHEN acceptance=FALSE THEN TRUE ELSE FALSE END)
        WHERE user_id = %(user_id)s;
        """,
        {
            "user_id": user_id
        }
    )


@data_connection.connection_handler
def change_reputation(cursor, user_id, value):
    cursor.execute(
        """
        UPDATE answer
        SET  vote_number = vote_number + %(value)s
        WHERE user_id=%(user_id)s
        """,
        {
            "user_id": user_id,
            "value": value
        }
    )

@data_connection.connection_handler
def select_user(cursor, user_id):
    cursor.execute(
        """
        SELECT * FROM users WHERE id=%(user_id)s;
        """,
        {
            "user_id": user_id
        }
    )
    return cursor.fetchone()

@data_connection.connection_handler
def get_one_comment(cursor, comment_id):
    cursor.execute("""
    SELECT * FROM comment WHERE id=%(comment_id)s;""", {'comment_id': comment_id})
    return cursor.fetchone()