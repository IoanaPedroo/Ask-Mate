from flask import Flask, render_template, request, url_for, redirect, session
import data_handler
import os
from werkzeug.utils import secure_filename
import bcrypt
from bonus_questions import SAMPLE_QUESTIONS
import questionn, answerr, commentt, tag, user


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


app.config["UPLOAD_FOLDER"] = os.path.join(
    "static",
    "images",
)


@app.route("/itdoesnot")
def stuff():
    return render_template("test.html")


@app.route("/itdoesnotmatter/<answer_id>/", methods=["POST"])
def acceptance_answers(answer_id):
    user_id = session["id"]
    answerr.accept_answer(answer_id, user_id)
    user.change_reputation(user_id=user_id, value=15)
    question_id = request.form.get("question_id")
    return redirect(url_for("display_question", question_id=question_id))


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_bytes_password)


@app.route("/list/<question_id>")
def display_question(question_id):
    if "id" in session:
        data_handler.increase_view_numbers(question_id)
        answers = answerr.get_answers(question_id)
        comments_a = [
            commentt.get_comments_for_answer(answer_id=answer["id"])
            for answer in answers
        ]
        print(comments_a)
        tags = tag.get_question_tags(question_id)
        return render_template(
            "question.html",
            question=questionn.get_question(question_id),
            answers=answers,
            question_id=question_id,
            comments=commentt.get_comments_for_question(question_id),
            comments_a=comments_a,
            user_id=session["id"],
            tags=tags,
        )
    return redirect(url_for("login_user"))


@app.route("/bonus-questions", methods=["GET", "POST"])
def bonus_q():
    search = request.form.get("doNotModifyThisId_QuestionsFilter")
    return render_template(
        "bonus_questions.html",
        questions=SAMPLE_QUESTIONS,
        user_id=session["id"],
    )


@app.route("/list/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):
    if request.method == "POST" and "email" in session:
        result = {
            "vote_number": 0,
            "message": request.form.get("message"),
            "question_id": question_id,
            "image": None,
            "user_id": session["id"],
        }
        data_handler.add_new_data_to_table(result, "answer")
        return redirect(url_for("display_question", question_id=question_id))

    return render_template(
        "new_answer.html",
        question_id=question_id,
        user_id=session["id"],
    )


@app.route("/list/<question_id>/delete", methods=["GET", "POST", "DELETE"])
def delete(question_id):
    questionn.delete_function(question_id)
    return redirect(url_for("list_q"))


@app.route("/<question_id>/<answer_id>/delete", methods=["GET", "POST", "DELETE"])
def delete_answer(question_id, answer_id):
    answerr.delete_answer(question_id, answer_id)
    return redirect(url_for("display_question", question_id=question_id))


def vote_question(id, count):
    questionn.vote_question(id, count)
    return redirect(url_for("display_question", question_id=id))


@app.route("/list/<question_id>/vote-up", methods=["GET", "POST"])
def vote_question_up(question_id):
    user_id = user.get_user(question_id)
    user.change_reputation(user_id=user_id['user_id'], value=5)
    return vote_question(question_id, "up")


@app.route("/list/<question_id>/vote-down", methods=["GET", "POST"])
def vote_question_down(question_id):
    user_id = user.get_user(question_id)
    user.change_reputation(user_id=user_id['user_id'], value=-2)
    return vote_question(question_id, "down")


@app.route("/list/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == "POST" and "email" in session:
        if "question_message" in request.form:
            new_message = request.form["question_message"]
            new_title = request.form["title"]
            questionn.edit_question(question_id, new_message, new_title)
            return redirect(url_for("display_question", question_id=question_id))
    return render_template(
        "edit.html",
        question=questionn.get_question(question_id),
        question_id=question_id,
        user_id=session["id"],
    )


@app.route("/")
def main_page():
    questions = questionn.get_last_five_question()
    return render_template("list.html", questions=questions)


@app.route("/list")
def list_q():
    order_by = request.args.get("order_by") if request.args.get("order_by") else "id"
    order_direction = (
        request.args.get("order_direction")
        if request.args.get("order_direction")
        else "ASC"
    )
    questions = questionn.sort_q(order_by, order_direction)
    return render_template("list.html", questions=questions)


@app.route("/add-question", methods=["GET", "POST"])
def add_q(id=None):
    if request.method == "POST" and "email" in session:
        result = {
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get("title"),
            "message": request.form.get("message"),
            "user_id": session["id"],
        }

        if request.files:
            image = request.files["images"]
            result["image"] = ""
            if image.filename != "":
                path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    secure_filename(image.filename),
                )
                image.save(app.root_path + "//" + path)
                result["image"] = "../" + path
        data_handler.add_new_data_to_table(result, "question")
        return redirect(url_for("list_q"))

    return render_template("add-question.html", id=id, user_id=session["id"])


def vote_answer(question_id, answer_id, count):
    answerr.vote_answer(answer_id, count)
    return redirect(
        url_for(
            "display_question",
            question_id=question_id,
            answer_id=answer_id,
        )
    )


@app.route("/list/<question_id>/<answer_id>/vote_up", methods=["GET", "POST"])
def vote_answer_up(question_id, answer_id):
    user_id = user.get_user_2(answer_id)
    user.change_reputation(user_id=user_id['user_id'], value=10)
    return vote_answer(question_id, answer_id, "up")


@app.route("/list/<question_id>/<answer_id>/vote-down", methods=["GET", "POST"])
def vote_answer_down(question_id, answer_id):
    user_id = user.get_user_2(answer_id)
    user.change_reputation(user_id=user_id['user_id'], value=-2)
    return vote_answer(question_id, answer_id, "down")


@app.route("/list/<question_id>/new-comment", methods=["GET", "POST"])
def new_comment_question(question_id):
    if request.method == "POST":
        if "editcomment" in request.form:
            result = {
                "question_id": question_id,
                "answer_id": None,
                "message": request.form.get("editcomment"),
                "edited_count": 0,
                "user_id": session["id"],
            }
            data_handler.add_new_data_to_table(result, "comment")
            return redirect(url_for("display_question", question_id=question_id))
    return render_template(
        "comment_q.html",
        question_id=question_id,
        user_id=session["id"],
    )


@app.route("/list/<question_id>/<answer_id>/new-comment", methods=["GET", "POST"])
def new_comment(question_id, answer_id):
    if request.method == "POST":
            result = {
                "question_id": None,
                "answer_id": answer_id,
                "message": request.form.get("newcomment"),
                "edited_count": 0,
                "user_id": session["id"]
            }
            data_handler.add_new_data_to_table(result,"comment")
            return redirect(
                url_for(
                    "display_question",
                    question_id=question_id,
                    answer_id=answer_id,
                )
            )

    return render_template(
        "new_comment.html",
        question_id=question_id,
        answer_id=answer_id,
        user_id=session["id"],
    )


@app.route("/list/<question_id>/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(question_id, answer_id):
    if request.method == "POST" and "email" in session:
        edited_answer = {
            "answer_id": answer_id,
            "question_id": question_id,
            "message": request.form.get("message"),
            "image": None,
        }
        answerr.edit_question_answer(edited_answer)
        return redirect(url_for("display_question", question_id=question_id))

    return render_template(
        "edit_answer.html",
        answer=answerr.get_answer(answer_id),
        answer_id=answer_id,
        question_id=question_id,
        user_id=session["id"],
    )


@app.route("/search", methods=["POST"])
def search_words():
    if request.method == "POST":
        search_phrase = request.form.get("search_phrase")

        posts = (
            data_handler.get_query(search_phrase)
            if search_phrase
            else questionn.get_questions()
        )

        return render_template("list.html", questions=posts, user_id=session["id"], search_phrase=search_phrase)



@app.route("/list/<question_id>/comment/<comment_id>/edit", methods=["GET", "POST"])
def edit_comment(question_id, comment_id):
    comment=commentt.get_one_comment(comment_id)
    if request.method == "POST":
        edited_comment = request.form.get('editcomment')
        commentt.edit_comments(comment,edited_comment)
        return redirect(url_for("display_question",question_id=question_id, user_id=session['id']))
    return render_template('edit_comment.html', comment_id=comment_id , comment=comment, question_id=question_id)


@app.route('/list/<question_id>/comment/<comment_id>/delete', methods=['GET', 'POST'])
def delete_comments(question_id,comment_id):
    commentt.delete_comment(comment_id)
    return redirect(url_for("display_question",question_id=question_id, user_id=session['id']))



@app.route("/registration", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        result = {
            "email": request.form.get("email"),
            "password": hash_password(request.form.get("password")),
        }
        user.add_user(result)
        return redirect(url_for("main_page"))
    return render_template("registered.html")


@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = data_handler.checkout_data(email)
        if verify_password(password, user["password"]):
            session.update({"email": user.get("email"), "id": user.get("id")})
            return redirect(url_for("main_page"))
        return "Invalid login attempt"
    return render_template("login_form.html")


@app.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("id", None)
    return redirect(url_for("main_page"))


@app.route("/users")
def list_users():
    if "id" in session:
        users = user.select_users()
        return render_template("list_users.html", users=users, user_id=session["id"])
    # user_id = None
    return redirect(url_for("main_page"))


@app.route("/user/<user_id>")
def user_page(user_id):
    if "email" in session:
        questions = user.count_q_by_user(user_id)
        answers = user.count_a_by_user(user_id)
        comments = user.count_c_by_user(user_id)
        all_questions = user.get_q_by_user(user_id)
        all_answers = user.get_a_by_user(user_id)
        all_comments = user.get_c_by_user(user_id)
        return render_template(
            "user_page.html",
            questions=questions,
            answers=answers,
            comments=comments,
            all_questions=all_questions,
            all_answers=all_answers,
            all_comments=all_comments,
            user_id=session["id"],
        )
    return redirect(url_for("main_page"))


@app.route("/list/<question_id>/new-tag", methods=["GET", "POST"])
def new_tag(question_id):
    if request.method == "POST":
        result={'name':request.form.get('message')}
        tag.add_tag(question_id, result)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_tag.html', question_id=question_id)

@app.route("/list/<question_id>/tag/<tag_id>/delete", methods=["GET", "POST"])
def delete_tag(question_id, tag_id):
    tag.delete_t(question_id, tag_id)
    return redirect(url_for("display_question",question_id=question_id, user_id=session['id']))


@app.route("/tag")
def list_tags():
    tags = tag.get_tags()
    return render_template("tags.html", tags=tags)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
