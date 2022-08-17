import data_connection
from datetime import datetime


@data_connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
    DELETE FROM comment WHERE id=%(comment_id)s""", {'comment_id':comment_id})

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
            "message": edited_comment,
            "submission_time": dt,
        },
    )

@data_connection.connection_handler
def get_one_comment(cursor, comment_id):
    cursor.execute(
        """
    SELECT * FROM comment WHERE id=%(comment_id)s;""",
        {"comment_id": comment_id},
    )
    return cursor.fetchone()
