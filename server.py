from flask import Flask, render_template, request, url_for, redirect
import data_manager

app = Flask(__name__)


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
            new_answer=request.form['message']
            data_manager.write_answer(new_answer, question_id)
        if 'question_message' in request.form:
            new_question=request.form['question_message']
            data_manager.write_question(qu)
    return render_template('question.html',question=data_manager.get_question(question_id), answers=data_manager.get_dict('sample_data/answer.csv'), )

@app.route('/question/<question_id>/delete')
def delete(question_id):
    data_manager.delete_function(question_id)
    return render_template('question.html')


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    answers=data_manager.get_dict('sample_data/answer.csv')
    for answer in answers:
        if answer['id'] == answer_id:
            answers.remove(answer)
    return redirect("/question/<question_id>")



@app.route('/question/<question_id>/edit')
def edit_question(question_id):
    return render_template('edit.html', question= data_manager.get_question(question_id))


if __name__ == "__main__":
    app.run(debug=True, # Allow verbose error reports
        port=5000 )