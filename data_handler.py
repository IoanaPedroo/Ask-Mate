import data_connection
from datetime import datetime


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
                "user_id": result["user_id"],
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
                "user_id": result["user_id"],
                "acceptance_answers": False,
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
                "user_id": result["user_id"],
            },
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
