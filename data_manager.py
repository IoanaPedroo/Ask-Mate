import csv

DATA_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "images",
]


def write(results):
    with open("sample_data/question.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()
        for story in results:
            writer.writerow(story)


def get_dict(file):
    results = []
    with open(file, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for element in reader:
            results.append(element)
    return results


def get_question(question_id):
    question = []
    results = get_dict(
        "/home/ioana/ask-mate-1-python-IoanaPedroo/sample_data/answer.csv"
    )
    for result in results:
        if result["id"] == question_id:
            question.append(result["title"])
            question.append(result["message"])
    return "    ".join(question)


def get_len(file):
    with open(file, "r") as file:
        files = file.read()
        lines = files.split("\n")
    number = len(lines)
    return number


def write_answer(new_answer, question_id):
    number = get_len("sample_data/answer.csv")
    with open("sample_data/answer.csv", "a") as file:
        file.write(
            f"\n{number},submission_time, vote_number,{question_id},{new_answer},images"
        )


def write_question(new_question, question_id):
    questions = get_dict("sample_data/question.csv")
    for question in questions:
        if question["id"] == question_id:
            question = new_question
    print(questions)


def delete_function(question_id):
    results = get_dict("sample_data/question.csv")
    for result in results:
        if result["id"] == question_id:
            results.remove(result)
    write(results)
