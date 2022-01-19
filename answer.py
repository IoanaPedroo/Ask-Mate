import data_connection
from datetime import datetime

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
def edit_question_answer(cursor, result):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        """
            UPDATE answer
            SET submission_time = %(submission_time)s, message = %(message)s
            WHERE id = %(answer_id)s AND question_id = %(question_id)s;
        """,
        {
            "question_id": result['question_id'],
            "answer_id": result['answer_id'],
            "message": result['message'],
            "submission_time": dt,
        },
    )


@data_connection.connection_handler
def accept_answer(cursor, answer_id, user_id):
    cursor.execute(
        """
        UPDATE answer
        SET acceptance = (CASE WHEN acceptance=FALSE THEN TRUE ELSE FALSE END)
        WHERE id = %(answer_id)s and user_id =%(user_id)s
        """,
        {"answer_id": answer_id, "user_id": user_id},
    )