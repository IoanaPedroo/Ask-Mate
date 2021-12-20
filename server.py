from flask import Flask, render_template, request, url_for, redirect
import data_handler
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(__file__),
    "static",
    "images",
)


@app.route("/")
def hello():
    return redirect(url_for("list_q"))


@app.route("/list/<question_id>", methods=["GET", "POST"])
def display_question(question_id):
    if request.method == "POST":
        if "message" in request.form:
            new_answer = request.form["message"]
            data_handler.write_answer(new_answer, question_id)

        if "question_message" in request.form:
            new_question = [request.form["question_message"], request.form["title"]]
            data_handler.write_question(new_question, question_id)

    return render_template(
        "question.html",
        question=data_handler.get_question(question_id),
        answers=data_handler.get_answers(question_id),
        question_id=question_id,
    )


@app.route("/list/<question_id>/new-answer")
def new_answer(question_id):
    return render_template("new_answer.html", question_id=question_id)


@app.route("/list/<question_id>/delete", methods=["GET", "POST", "DELETE"])
def delete(question_id):
    data_handler.delete_function(question_id)
    return redirect(url_for("list_q"))


@app.route("/<question_id>/<answer_id>/delete", methods=["GET", "POST", "DELETE"])
def delete_answer(answer_id, question_id):
    data_handler.delete_answer(answer_id, question_id)
    return redirect(url_for("display_question", question_id=question_id))


def vote_question(id, count):
    data_handler.vote_question(id, count)
    return redirect(url_for("display_question", question_id=id))


@app.route("/list/<question_id>/vote-up", methods=["GET", "POST"])
def vote_question_up(question_id):
    return vote_question(question_id, 1)


@app.route("/list/<question_id>/vote-down", methods=["GET", "POST"])
def vote_question_down(question_id):
    return vote_question(question_id, -1)


@app.route("/list/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    return render_template(
        "edit.html",
        question=data_handler.get_question(question_id),
        question_id=question_id,
    )


@app.route("/list")
def list_q():
    questions = data_handler.get_questions("sample_data/question.csv")
    header = data_handler.DATA_HEADER
    order_by = request.args.get("order_by") if request.args.get("order_by") else "title"
    order_direction = (
        request.args.get("order_direction")
        if request.args.get("order_direction")
        else "ASC"
    )

    questions = data_handler.sort_q(questions, order_by, order_direction)
    return render_template("list.html", questions=questions, header=header)


@app.route("/add-question", methods=["GET", "POST"])
def add_q(id=None):
    if request.method == "POST":
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
                path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    secure_filename(image.filename),
                )
                image.save(path)
                result["images"] = "../static/images/" + secure_filename(image.filename)
        questions.append(result)

        data_handler.save_data_to_csv(
            questions,
            "sample_data/question.csv",
            data_handler.DATA_HEADER,
        )
        return redirect(url_for("list_q"))
    return render_template("add-question.html", id=id)


def vote_answer(qid, aid, count):
    data_handler.vote_answer(qid, aid, count)
    return redirect(url_for("display_question", question_id=qid))


@app.route("/list/<question_id>/<answer_id>/vote_up", methods=["GET", "POST"])
def vote_answer_up(question_id, answer_id):
    return vote_answer(question_id, answer_id, 1)


@app.route("/list/<question_id>/<answer_id>/vote-down", methods=["GET", "POST"])
def vote_answer_down(question_id, answer_id):
    return vote_answer(question_id, answer_id, -1)


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Allow verbose error reports
