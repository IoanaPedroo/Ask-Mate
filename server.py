from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list")
def list_q():
    questions = data_handler.get_questions("/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/question.csv")
    header = data_handler.DATA_HEADER
    return render_template('list.html', questions=questions, header=header)

@app.route("/add-question", methods = ["GET", "POST"])
def add_q(id=None):
    if request.method == 'GET':
        return render_template('add-question.html', id=id)
    elif request.method == 'POST':
        questions = data_handler.get_questions("/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/question.csv")
        result = {}
        result['id'] = len(questions)+1
        result['submission_time'] = request.form.get('submission_time')
        result['view_number'] = request.form.get('view_number')
        result['vote_number'] = request.form.get('vote_number')
        result['title'] = request.form.get('title')
        result['message'] = request.form.get('message')
        result['image'] = request.files('image')
        questions.append(result)
        data_handler.save_data_to_csv(questions, "/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/question.csv")
        return redirect("/question/<question_id>")

@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"]
def delete_answer(answer_id):
    answers = data_handler.get_all_user_story("/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv")
    for answer in answers:
        if answer['id'] == answer_id:
            answers.remove(answer)
            data_handler.save_data_to_csv(answers, "/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv")
    return redirect("/question/<question_id>")

def upload_image():
    if 'image' not in request.files:
        flash('No file apart')
        return redirect('/add-question')
    image = request.files['image']
    if file.filename == '':
        flash('No image selected for uploding')
        return redirect('/add-question')
    if file and allowe_file(file.filename):
        filename = secure_filename(file.filename)
if __name__ == "__main__":
    app.run()
