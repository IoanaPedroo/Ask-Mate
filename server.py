from flask import Flask, render_template, request, url_for, redirect
import data_manager
import data_handler
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "static", "images")


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    return render_template('new_answer.html', new_answer=new_answer, question_id=question_id)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    if request.method=="POST":
        if 'message' in request.form:
            new_answer = request.form['message']
            data_manager.write_answer(new_answer, question_id)
        if 'question_message' in request.form:
            new_question=request.form['question_message']
            data_manager.write_question(new_question, question_id)
        answers=data_handler.get_questions('sample_data/answer.csv')

    for answer in answers:
        if answer['id'] == answer_id:
            answer['vote_number'] = int(answer['vote_number'])+1
            data_handler.save_data_to_csv(answers,"sample_data/answer.csv", data_handler.DATA_HEADER1)
    return render_template('question.html',question=data_manager.get_question(question_id), answers=data_manager.get_dict('sample_data/answer.csv') )

@app.route('/question/<question_id>/delete')
def delete(question_id):
    data_manager.delete_function(question_id)
    return render_template('question.html')


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    answers = data_handler.get_all_user_story("sample_data/answer.csv")
    for answer in answers:
        if answer['id'] == answer_id:
            answers.remove(answer)
            data_handler.save_data_to_csv(answers, "sample_data/answer.csv",  data_handler.DATA_HEADER1)
    return redirect("/question/<question_id>")

# @app.route('/question/<answer_id>/vote_up', methods=["GET", "POST"])
# def vote_up(answer_id):
#     answers=data_handler.get_questions('sample_data/answer.csv')
#     print(request.args)
#     for answer in answers:
#         if answer['id']==answer_id:
#             answer['vote_number'] = int( answer['vote_number'])+1
#             data_handler.save_data_to_csv(answers,"sample_data/answer.csv", data_handler.DATA_HEADER1)
#     return render_template('question.html')


# @app.route('/question/<answer_id>/vote_down',methods=["GET", "POST"])
# def vote_down(answer_id):
#     answers=data_handler.get_questions('sample_data/answer.csv')
#     for answer in answers:
#         if answer['id']==answer_id:
#             answer['vote_number'] =  int( answer['vote_number'])-1
#             data_handler.save_data_to_csv(answers,"sample_data/answer.csv", data_handler.DATA_HEADER1)
#     return render_template('question.html')




@app.route('/question/<question_id>/edit')
def edit_question(question_id):
    return render_template('edit.html', question= data_manager.get_question(question_id))


@app.route("/list")
def list_q():
    questions = data_handler.get_questions("sample_data/question.csv")
    header = data_handler.DATA_HEADER
    return render_template('list.html', questions=questions, header=header)

@app.route("/add-question", methods = ["GET", "POST"])
def add_q(id=None):
    if request.method == 'GET':
        return render_template('add-question.html', id=id)
    elif request.method == 'POST':
        questions = data_handler.get_questions("sample_data/question.csv")
        result = {}
        result['id'] = len(questions)+1
        result['submission_time'] = request.form.get('submission_time')
        result['view_number'] = request.form.get('view_number')
        result['vote_number'] = request.form.get('vote_number')
        result['title'] = request.form.get('title')
        result['message'] = request.form.get('message')
        print(request.files)
        if request.files:
            image = request.files['images']
            if image.filename != '':
                path = secure_filename(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                image.save(path)
            result['images'] = image
        questions.append(result)
        data_handler.save_data_to_csv(questions, "sample_data/question.csv", data_handler.DATA_HEADER)
        return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True, # Allow verbose error reports
        port=5000 )