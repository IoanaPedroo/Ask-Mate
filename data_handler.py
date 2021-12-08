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


