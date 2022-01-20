import data_connection


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
def get_question(cursor, question_id):
    cursor.execute(
        "SELECT * FROM question where id = %(question_id)s;",
        {"question_id": question_id},
    )
    return cursor.fetchone()



@data_connection.connection_handler
def delete_function(cursor, question_id):
    cursor.execute(
        """
            DELETE FROM comment
            WHERE comment.answer_id IN (SELECT answer.id FROM answer WHERE answer.question_id = %(question_id)s);

            DELETE FROM answer
            WHERE question_id = %(question_id)s;
            
            DELETE FROM question_tag
            WHERE question_id = %(question_id)s;
            
            DELETE FROM comment
            WHERE question_id = %(question_id)s;

            DELETE FROM question
            WHERE id = %(question_id)s;
       """,
        {"question_id": question_id},
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
