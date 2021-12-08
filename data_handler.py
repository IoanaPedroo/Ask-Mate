import csv
from operator import itemgetter

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '/home/ioana/ask-mate-1-python-IoanaPedroo/static/image'


def get_questions(file):
    result = []
    with open(file, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for element in reader:
            result.append(element)
    final = sorted(result, key=itemgetter('id'), reverse=True)
    return final


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_data_to_csv(story_database, file):
    with open(file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
        writer.writeheader()
        for story in story_database:
            writer.writerow(story)


