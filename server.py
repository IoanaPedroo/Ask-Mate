from flask import Flask, render_template, request, url_for, redirect
import data_handler
import os
from werkzeug.utils import secure_filename
import bcrypt


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(
    "static",
    "images",
)

app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(__file__),
    "static",
    "images",
)


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@app.route("/list/<question_id>")
def display_question(question_id):
    data_handler.increase_view_numbers(question_id)
    answers = data_handler.get_answers(question_id)
    comm = [
        data_handler.get_comments_for_answer(answer_id=answer["id"])
        for answer in answers
    ]

    return render_template(
        "question.html",
        question=data_handler.get_question(question_id),
        answers=answers,
        question_id=question_id,
        comments=data_handler.get_comments_for_question(question_id),
        comments_a=comm,
    )


@app.route("/bonus-questions")
def bonus_q():
    return render_template("bonus_questions.html", questions=SAMPLE_QUESTIONS)


@app.route("/list/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):
    if request.method == "POST":
        result = {
            "vote_number": 0,
            "message": request.form.get("message"),
            "question_id": question_id,
            "image": None,
        }
        data_handler.add_new_data_to_table(result, "answer")
        return redirect(url_for("display_question", question_id=question_id))

    return render_template("new_answer.html", question_id=question_id)


@app.route("/list/<question_id>/delete", methods=["GET", "POST", "DELETE"])
def delete(question_id):
    data_handler.delete_function(question_id)
    return redirect(url_for("list_q"))


@app.route("/<question_id>/<answer_id>/delete", methods=["GET", "POST", "DELETE"])
def delete_answer(question_id, answer_id):
    data_handler.delete_answer(question_id, answer_id)
    return redirect(url_for("display_question", question_id=question_id))


def vote_question(id, count):
    data_handler.vote_question(id, count)
    return redirect(url_for("display_question", question_id=id))


@app.route("/list/<question_id>/vote-up", methods=["GET", "POST"])
def vote_question_up(question_id):
    return vote_question(question_id, "up")


@app.route("/list/<question_id>/vote-down", methods=["GET", "POST"])
def vote_question_down(question_id):
    return vote_question(question_id, "down")


@app.route("/list/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == "POST":
        if "question_message" in request.form:
            new_message = request.form["question_message"]
            new_title = request.form["title"]
            data_handler.edit_question(question_id, new_message, new_title)
            return redirect(url_for("display_question", question_id=question_id))
    return render_template(
        "edit.html",
        question=data_handler.get_question(question_id),
        question_id=question_id,
    )


@app.route("/")
def main_page():
    questions = data_handler.get_last_five_question()
    return render_template("list.html", questions=questions)


@app.route("/list")
def list_q():
    order_by = request.args.get("order_by") if request.args.get("order_by") else "id"
    order_direction = (
        request.args.get("order_direction")
        if request.args.get("order_direction")
        else "ASC"
    )
    questions = data_handler.sort_q(order_by, order_direction)
    return render_template("list.html", questions=questions)


@app.route("/add-question", methods=["GET", "POST"])
def add_q(id=None):
    if request.method == "POST":
        result = {
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get("title"),
            "message": request.form.get("message"),
        }

        if request.files:
            image = request.files["images"]
            result["image"] = ""
            if image.filename != "":
                path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    secure_filename(image.filename),
                )
                image.save(path)
                result["image"] = os.path.join(
                    UPLOAD_FOLDER,
                    secure_filename(image.filename),
                )

        data_handler.add_new_data_to_table(result, "question")
        return redirect(url_for("list_q"))

    return render_template("add-question.html", id=id)


def vote_answer(question_id, answer_id, count):
    data_handler.vote_answer(answer_id, count)
    return redirect(
        url_for(
            "display_question",
            question_id=question_id,
            answer_id=answer_id,
        )
    )


@app.route("/list/<question_id>/<answer_id>/vote_up", methods=["GET", "POST"])
def vote_answer_up(question_id, answer_id):
    return vote_answer(question_id, answer_id, "up")


@app.route("/list/<question_id>/<answer_id>/vote-down", methods=["GET", "POST"])
def vote_answer_down(question_id, answer_id):
    return vote_answer(question_id, answer_id, "down")


@app.route("/list/<question_id>/new-comment", methods=["GET", "POST"])
def new_comment_a(question_id):
    if request.method == "POST":
        result = {
            "question_id": question_id,
            "answer_id": None,
            "message": request.form.get("message"),
            "edited_count": 0,
        }
        data_handler.add_new_data_to_table(result, "comment")
        return redirect(url_for("display_question", question_id=question_id))

    return render_template("comment_q.html", question_id=question_id)


@app.route("/list/<question_id>/<answer_id>/new-comment", methods=["GET", "POST"])
def new_comment(question_id, answer_id):
    if request.method == "POST":
        result = {
            "question_id": None,
            "answer_id": answer_id,
            "message": request.form.get("message"),
            "edited_count": 0,
        }
        data_handler.add_new_data_to_table(result, "comment")
        return redirect(url_for("display_question", question_id=question_id))

    return render_template(
        "new_comment.html",
        question_id=question_id,
        answer_id=answer_id,
    )


@app.route("/list/<question_id>/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(question_id, answer_id):
    if request.method == "POST":
        edited_answer = {
            "answer_id": answer_id,
            "question_id": question_id,
            "message": request.form.get("message"),
            "image": None,
        }
        data_handler.edit_question_answer(edited_answer)
        return redirect(url_for("display_question", question_id=question_id))

    return render_template(
        "edit_answer.html",
        answer=data_handler.get_answer(answer_id),
        answer_id=answer_id,
        question_id=question_id,
    )


@app.route("/search", methods=["POST"])
def search_words():
    if request.method == "POST":
        search_phrase = request.form.get("search_phrase")

        posts = (
            data_handler.get_query(search_phrase)
            if search_phrase
            else data_handler.get_questions()
        )

        return render_template("list.html", questions=posts)


@app.route("/list/<question_id>/<comment_id>/edit", methods=["GET", "POST"])
def edit_comment(question_id, comment_id):
    if request.method == "POST":
        updated_comment = request.form.get("message")
        data_handler.edit_comment(comment_id, updated_comment)
        return redirect(url_for("display_question", question_id=question_id))

@app.route("/registration", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        result = {
            "email": request.form.get('email'),
            "password":  hash_password(request.form.get('password')),
        }
        data_handler.add_user(result)
        return redirect(url_for('main_page'))
    return render_template('registered.html')
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/login", methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = data_handler.checkout_data(email)
        if verify_password(password, user['password']):
            session.update({'email': user.get('email')})
            return redirect(url_for('main_page'))
        return 'Invalid login attempt'
    return render_template('login_form.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('main_page'))

@app.route('/users')
def list_users():
    users = data_handler.select_users
    return render_template('list_users.html', users=users)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
