import csv
from operator import itemgetter
import os
import sys

DATA_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "image",
]
DATA_HEADER1 = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image",
]


def sort_q(questions, order_by, order_direction):
    if order_direction == "ASC":
        order_direction = False
    elif order_direction == "DESC":
        order_direction = True
    print(order_direction)
    questions = sorted(questions, key=lambda t: t[order_by], reverse=order_direction)
    return questions
  
        
def get_questions(file):
    result = []
    with open(f"{os.path.dirname(sys.argv[0])}/{file}", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for element in reader:
            result.append(element)
    result = sorted(result, key=itemgetter("id"), reverse=True)
    return result


def save_data_to_csv(story_database, file, data):
    with open(f"{os.path.dirname(sys.argv[0])}/{file}", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data)
        writer.writeheader()
        for story in story_database:
            writer.writerow(story)


def write(results):
    with open('sample_data/question.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()
        for story in results:
            writer.writerow(story) 


def get_answers(question_id):
    answers=[]
    results = get_questions('sample_data/answer.csv')
    for element in results:
           if element['question_id']==question_id:
            answers.append(element)
    return answers


def get_question(question_id):
    question=[]
    results = get_questions('sample_data/question.csv')
    for result in results:
        if result['id']==question_id:
            return result


def get_len(file):
    with open(file,'r') as file:
        files=file.read()
        lines=files.split('\n')
    number=len(lines)
    return number


def write_answer(new_answer, question_id):
    number=get_len('sample_data/answer.csv')
    with open('sample_data/answer.csv', 'a') as file:
        file.write(f'\n{number},submission_time, {0},{question_id},{new_answer},image')
      

def write_question(new_question, question_id):
    questions=get_questions('sample_data/question.csv')
    for question in questions:
        if question['id']==question_id:
            question['message']=new_question[0]
            question['title']=new_question[1]
    write(questions)
    

def delete_function(question_id):
    results = get_questions('sample_data/question.csv')
    for result in results:
        if result['id']==question_id:
            results.remove(result)
    write(results) 


def delete_answer(answer_id, question_id):
    answers=get_answers(question_id)
    for answer in answers:
        if answer['id'] == answer_id:
            answers.remove(answer)
            save_data_to_csv(answers, "sample_data/answer.csv",  DATA_HEADER1)



def vote_q_up(question_id):
    questions=get_questions('sample_data/question.csv')
    for question in questions:
        if question['id']==question_id:
            question['vote_number'] = int(question['vote_number'])+1
    write(questions)



def vote_q_down(question_id):
    questions=get_questions('sample_data/question.csv')
    for question in questions:
        if question['id']==question_id:
            question['vote_number'] = int(question['vote_number'])-1
    write(questions)


def vote_a_up(question_id,answer_id):
    answers=get_answers(question_id)
    for answer in answers:
        if answer['id']==answer_id:
            answer['vote_number'] = int(answer['vote_number'])+1
    with open('sample_data/answer.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER1)
        writer.writeheader()
        for story in answers:
            if story['question_id']==question_id:
                writer.writerow(story)


def vote_a_down(question_id,answer_id):
    answers=get_answers(question_id)
    for answer in answers:
        if answer['id']==answer_id:
            answer['vote_number'] = int(answer['vote_number'])-1
    with open('sample_data/answer.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER1)
        writer.writeheader()
        for story in answers:
            if story['question_id']==question_id:
                writer.writerow(story)