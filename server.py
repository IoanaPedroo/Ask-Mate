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
    return "Hello World!"


@app.route('/list/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    if request.method=="POST":
        if 'message' in request.form:
            new_answer = request.form['message']
            data_handler.write_answer(new_answer, question_id)
        if 'question_message' in request.form:
            new_question=[request.form['question_message'],request.form['title']] 
            data_handler.write_question(new_question, question_id)
        answers=data_handler.get_answers(question_id)
    return render_template('question.html',question=data_handler.get_question(question_id), answers=data_handler.get_answers(question_id), question_id=question_id )


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


@app.route('/list/<question_id>/vote-up',methods=["GET", "POST"])
def vote_question_up(question_id):
    data_handler.vote_q_up(question_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/list/<question_id>/vote-down',methods=["GET", "POST"])
def vote_question_down(question_id):
    data_handler.vote_q_down(question_id)
    return redirect(url_for('display_question', question_id=question_id))   




@app.route('/list/<question_id>/edit', methods=['GET', "POST"])
def edit_question(question_id):
    return render_template('edit.html', question= data_handler.get_question(question_id), question_id=question_id)
   


@app.route("/list")
def list_q():
    questions = data_handler.get_questions("sample_data/question.csv")
    header = data_handler.DATA_HEADER
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
        questions.insert(0, result)
        data_handler.save_data_to_csv(
            questions, "sample_data/question.csv", data_handler.DATA_HEADER
        )
        return redirect("/list")


@app.route('/list/<question_id>/<answer_id>/vote_up',  methods=['GET', "POST"])
def vote_answer_up(question_id, answer_id):
    data_handler.vote_a_up(question_id,answer_id)
    return redirect(url_for('display_question', question_id=question_id))



@app.route('/list/<question_id>/<answer_id>/vote-down',  methods=['GET', "POST"])
def vote_answer_down(question_id, answer_id):
    data_handler.vote_a_down(question_id,answer_id)
    return redirect(url_for('display_question', question_id=question_id))



if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Allow verbose error reports
