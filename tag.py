import data_connection
from datetime import datetime

@data_connection.connection_handler
def add_tag(cursor, question_id, result):
    cursor.execute(
        """
        INSERT INTO tag(name) VALUES(%(result)s);
        INSERT INTO question_tag (question_id, tag_id)
        SELECT %(question_id)s,tag.id FROM tag
        WHERE name=%(result)s""",{
                'result':result['name'],
                "question_id": question_id,
            }
    )


@data_connection.connection_handler
def delete_t(cursor, question_id, tag_id):
    cursor.execute("""
    DELETE FROM question_tag WHERE question_id=%(question_id)s AND tag_id=%(tag_id)s""", {'question_id':question_id, 'tag_id':tag_id})


@data_connection.connection_handler
def get_tags(cursor):
    cursor.execute("""
    SELECT name, COUNT(question.id) FROM tag
    inner join question_tag on tag.id = question_tag.tag_id
    inner join question on question.id = question_tag.question_id
    group by name;
    """)
    return cursor.fetchall()


@data_connection.connection_handler
def get_question_tags(cursor, question_id):
    cursor.execute("""
    SELECT tag.name, tag.id FROM tag
    LEFT OUTER JOIN question_tag ON tag.id = question_tag.tag_id
    LEFT OUTER JOIN question on question.id = question_tag.question_id
    WHERE question_tag.question_id = %(question_id)s
    """,
       {"question_id": question_id},
       )
    return cursor.fetchall()