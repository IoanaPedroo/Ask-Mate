import data_connection


@data_connection.connection_handler
def sort_q(cursor, order_by, order_direction):
    cursor.execute(f"""
                        SELECT * FROM question 
                        ORDER BY {order_by} {order_direction};
                        """)
    return cursor.fetchall()


@data_connection.connection_handler
def get_questions(cursor):
    query = """
        SELECT * FROM question
    """
    cursor.execute(query)
    return cursor.fetchall()


@data_connection.connection_handler
def get_answers(cursor, question_id):
    query = """
            SELECT * FROM answer
            WHERE question_id=%(question_id)s
            ORDER BY id;
        """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@data_connection.connection_handler
def get_question(cursor, question_id):
    query = """
        SELECT * FROM question where id = %(question_id)s;
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()

@data_connection.connection_handler
def add_new_data_to_table(cursor, result, content):
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    if content == "question":
        cursor.execute("""
                        INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                        VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                         """,
                       {'submission_time': date,
                        'view_number': result['view_number'],
                        'vote_number': result['vote_number'],
                        'title': result['title'],
                        'message': result['message'],
                        'image': result['image']})
    elif content == "answer":
        cursor.execute("""
                        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                        VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                        """,
                       {'submission_time': date,
                        'vote_number': result['vote_number'],
                        'question_id': result['question_id'],
                        'message': result['message'],
                        'image': result['image']}
                       )

    elif content == "comment":
        cursor.execute("""
                        INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count)
                        VALUES(%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);
                        """,
                       {'question_id': result['question_id'],
                        'answer_id': result['answer_id'],
                        'message': result['message'],
                        'submission_time': date,
                        'edited_count': result['edited_count']}
                       )


@data_connection.connection_handler
def delete_function(cursor, question_id):
    query = """
    DELETE FROM comment
       WHERE question_id = %(question_id)s;
       
       DELETE FROM answer
       WHERE question_id = %(question_id)s;
       
       DELETE FROM question_tag
       WHERE question_id = %(question_id)s;
       
       DELETE FROM question
       WHERE id = %(question_id)s;
       """
    cursor.execute(query, {'question_id': question_id})


@data_connection.connection_handler
def delete_answer(cursor, question_id, answer_id):
    query = """
                DELETE FROM comment
                WHERE question_id = %(question_id)s AND answer_id = %(answer_id)s;
                DELETE FROM answer
                WHERE id = %(answer_id)s;
                """
    cursor.execute(query, {'question_id': question_id, 'answer_id': answer_id})

@data_connection.connection_handler
def vote_question(cursor, question_id, count):
    if count == 'up':
        query = """
        UPDATE question SET vote_number = vote_number + 1
        WHERE id = %(question_id)s;
        """
    else:
        query = """
                UPDATE question SET vote_number = vote_number - 1
                WHERE id = %(question_id)s;
                """
    cursor.execute(query, {'question_id': question_id})


@data_connection.connection_handler
def vote_answer(cursor, answer_id, count):
    if count == 'up':
        query = """
            UPDATE answer
            SET vote_number = vote_number + 1
            WHERE id = %(answer_id)s;
            """
    else:
        query = """
            UPDATE answer
            SET vote_number = vote_number - 1
            WHERE id = %(answer_id)s;
            """
    cursor.execute(query, {'answer_id': answer_id})


@data_connection.connection_handler
def edit_question(cursor, question_id, edited_title, edited_message):
    query = """
            UPDATE question
            SET title = %(edited_title)s, message = %(edited_message)s
            WHERE id = %(question_id)s;
            """
    cursor.execute(query, {'question_id': question_id, 'edited_title': edited_title, 'edited_message': edited_message})

