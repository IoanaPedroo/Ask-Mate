import data_manager
from flask import Flask, render_template, request, redirect, flash, url_for
import data_handler
from operator import itemgetter
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/ioana/ask-mate-1-python-IoanaPedroo/static/image"

def sort_q():
    sorter = request.args('order_by')
    order = request.args('order_direction')
    questions = data_handler.get_questions("/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/question.csv")
    if order == "DESC":
        final = sorted(questions, key=itemgetter(sorter), reverse=True)
        return final
    final = sorted(questions, key=itemgetter(sorter))
    return final

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    return render_template('new_answer.html', new_answer=new_answer)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    if request.method=="POST":
        if 'message' in request.form:
            new_answer = request.form['message']
            data_manager.write_answer(new_answer, question_id)
        if 'question_message' in request.form:
            new_question = request.form['question_message']
            data_manager.write_question(new_question)
    return render_template('question.html',question=data_manager.get_question(question_id), answers=data_manager.get_dict("/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv"))

@app.route('/question/<question_id>/delete')
def delete(question_id):
    data_manager.delete_function(question_id)
    return render_template('question.html')


# @app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
# def delete_answer(answer_id):
#     answers=data_manager.get_dict('sample_data/answer.csv')
#     for answer in answers:
#         if answer['id'] == answer_id:
#             answers.remove(answer)
#     return redirect("/question/<question_id>")



@app.route('/question/<question_id>/edit')
def edit_question(question_id):
    return render_template('edit.html', question= data_manager.get_question(question_id))


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
        result['image'] = request.files['image']
        if result['image'].filename == '':
            flash('No selected file')
            return redirect(request.url)
        if result['image'] and data_handler.allowed_file(result['image'].filename):
            filename = secure_filename(result['image'].filename)
            result['image'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
        questions.append(result)
        data_handler.save_data_to_csv(questions, "/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/question.csv")
        return redirect("/list")

@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    answers = data_handler.get_all_user_story("/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv")
    for answer in answers:
        if answer['id'] == answer_id:
            answers.remove(answer)
            data_handler.save_data_to_csv(answers, "/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv")
    return redirect("/question/<question_id>")

# /question/<question_id>/vote_up
# /question/<question_id>/vote_down
# /answer/<answer_id>/vote_up
# /answer/<answer_id>/vote_down

if __name__ == "__main__":
    app.run(debug=True, # Allow verbose error reports
        port=5000 )