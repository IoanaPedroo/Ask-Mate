from flask import Flask, render_template, request, url_for, redirect
import data_manager
import data_handler

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
        if 'question_message' in request.form:
            new_question=request.form['question_message']
            data_manager.write_question(new_question, question_id)
    return render_template('question.html',question=data_manager.get_question(question_id), answers=data_manager.get_dict('sample_data/answer.csv') )

@app.route('/question/<question_id>/delete')
def delete(question_id):
    data_manager.delete_function(question_id)
    return render_template('question.html')


# @app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
# def delete_answer(answer_id):
#     answers = data_handler.get_all_user_story("/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv")
#     for answer in answers:
#         if answer['id'] == answer_id:
#             answers.remove(answer)
#             data_handler.save_data_to_csv(answers, "/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv",  data_handler.DATA_HEADER1)
#     return redirect("/question/<question_id>")

# @app.route('/question/<question_id>/answers', methods=["GET", "POST"])
# def answer(answer_id, question_id):
#     if request.method=="POST":
#      if 'message' in request.form:
#             new_answer=request.form['message']
#             data_manager.write_answer(new_answer, question_id)
#     # answers=data_handler.get_questions('sample_data/answer.csv')
#     # print(request.args)
#     # for answer in answers:
#     #     if answer['id']==answer_id:
#     #         answer['vote_number'] = int( answer['vote_number'])+1
#     #         data_handler.save_data_to_csv(answers, 'sample_data/answer.csv', data_handler.DATA_HEADER1)
#     return render_template('anwers.html',  answers=data_manager.get_dict('sample_data/answer.csv' ))




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
        #result['image'] = request.files('image')
        questions.append(result)
        data_handler.save_data_to_csv(questions, "/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/question.csv",  data_handler.DATA_HEADER)
        return redirect("/question/<question_id>")



# def upload_image():
#     if 'image' not in request.files:
#         flash('No file apart')
#         return redirect('/add-question')
#     image = request.files['image']
#     if file.filename == '':
#         flash('No image selected for uploding')
#         return redirect('/add-question')
#     if file and allowe_file(file.filename):
#         filename = secure_filename(file.filename)
#     pass


if __name__ == "__main__":
    app.run(debug=True, # Allow verbose error reports
        port=5000 )