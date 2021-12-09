import csv

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER1=['id','submission_time','vote_number','question_id','message','image']
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def get_questions(file):
    result = []
    with open(file, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for element in reader:
            result.append(element)
    return result


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_data_to_csv(story_database, file, data):
    with open(file, 'w', newline='') as csv_file:
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
            question.append(result['title'])
            question.append(result['message'])
    return question


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