import csv
from operator import itemgetter
import os
import sys

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'images']
DATA_HEADER1=['id','submission_time','vote_number','question_id','message','images']
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '/home/ioana/ask-mate-1-python-IoanaPedroo/static/images'


def get_questions(file):
    result = []
    with open(f"{os.path.dirname(sys.argv[0])}/{file}", newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for element in reader:
            result.append(element)
    final = sorted(result, key=itemgetter('id'), reverse=True)
    return final


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_data_to_csv(story_database, file, data):
    with open(f"{os.path.dirname(sys.argv[0])}/{file}", 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data)
        writer.writeheader()
        for story in story_database:
            writer.writerow(story)


