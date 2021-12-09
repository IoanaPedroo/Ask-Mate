from flask import Flask, render_template, request, url_for, redirect
import data_handler
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(__file__), "static", "images"
)


@app.route("/")
def hello():
    return redirect("/list")


@app.route('/list/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    if request.method=="POST":
        if 'message' in request.form:
            new_answer = request.form['message']
            data_handler.write_answer(new_answer, question_id)
        if 'question_message' in request.form:
            new_question=[request.form['question_message'],request.form['title']] 
            data_handler.write_question(new_question, question_id)
    return render_template('question.html',question=data_handler.get_question(question_id), answers=data_handler.get_answers(question_id), question_id=question_id)


@app.route('/list/<question_id>/new-answer')
def new_answer(question_id):
    return render_template('new_answer.html', question_id=question_id)


@app.route('/list/<question_id>/delete', methods=['GET', 'POST'])
def delete(question_id):
    data_handler.delete_function(question_id)
    return render_template('question.html', question_id=question_id)


@app.route("/<question_id>/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id, question_id):
    data_handler.delete_answer(answer_id, question_id)
    return redirect(url_for('display_question', question_id=question_id))

# @app.route('/question/<question_id>/answers', methods=["GET", "POST"])
# def answer(answer_id, question_id):
#     if request.method=="POST":
#      if 'message' in request.form:
#             new_answer=request.form['message']
#             data_handler.write_answer(new_answer, question_id)
#     # answers=data_handler.get_questions('sample_data/answer.csv')
#     # print(request.args)
#     # for answer in answers:
#     #     if answer['id']==answer_id:
#     #         answer['vote_number'] = int( answer['vote_number'])+1
#     #         data_handler.save_data_to_csv(answers, 'sample_data/answer.csv', data_handler.DATA_HEADER1)
#     return render_template('anwers.html',  answers=data_handler.get_dict('sample_data/answer.csv' ))




# @app.route('/question/<question_id>/answers/vote',methods=["GET", "POST"])
# def vote():
#     if vote=='LIKE':
#         answers=data_handler.get_questions('sample_data/answer.csv')
#         for answer in answers:
#             if answer['id']==answer_id:
#                 answer['vote_number'] =  int( answer['vote_number'])+1
#                 data_handler.save_data_to_csv(answers, 'sample_data/answer.csv', data_handler.DATA_HEADER1)
#     elif vote=='HATRED':
#         for answer in answers:
#             if answer['id']==answer_id:
#                 answer['vote_number'] =  int( answer['vote_number'])-1
#                 data_handler.save_data_to_csv(answers, 'sample_data/answer.csv', data_handler.DATA_HEADER1)
#     return render_template('answers.html')




@app.route('/list/<question_id>/edit', methods=['GET', "POST"])
def edit_question(question_id):
    return render_template('edit.html', question= data_handler.get_question(question_id), question_id=question_id)
   


@app.route("/list")
def list_q():
    questions = data_handler.get_questions("sample_data/question.csv")
    header = data_handler.DATA_HEADER
    order_by = "title"
    if request.args.get("order_by"):
        order_by = request.args.get("order_by")
    order_direction = "ASC"
    if request.args.get("order_direction"):
        order_direction = request.args.get("order_direction")
    questions = data_handler.sort_q(questions, order_by, order_direction)
    return render_template("list.html", questions=questions, header=header)


@app.route("/add-question", methods=["GET", "POST"])
def add_q(id=None):
    if request.method == "GET":
        return render_template("add-question.html", id=id)
    elif request.method == "POST":
        questions = data_handler.get_questions("sample_data/question.csv")
        result = {}
        result["id"] = len(questions) + 1
        result["submission_time"] = request.form.get("submission_time")
        result["view_number"] = request.form.get("view_number")
        result["vote_number"] = request.form.get("vote_number")
        result["title"] = request.form.get("title")
        result["message"] = request.form.get("message")
        if request.files:
            image = request.files["images"]
            if image.filename != "":
                path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(image.filename))
                image.save(path)
                result["images"] = "../static/images/" + secure_filename(image.filename)
        questions.append(result)
        data_handler.save_data_to_csv(
            questions, "sample_data/question.csv", data_handler.DATA_HEADER
        )
        return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Allow verbose error reports
