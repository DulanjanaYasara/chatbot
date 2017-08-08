from pymongo import MongoClient

client = MongoClient()
# client = MongoClient("mongodb://mongodb0.example.net:27017")

# Access database objects
db = client.answerComparison
col_answer_given = db.anwered
col_answer_not_given = db.unanswered


def remove_data():
    # Removing the existing data
    col_answer_given.remove()
    col_answer_not_given.remove()


def export_q_a(question_intent, answer, bot_answer, answered):
    # Insert document into a collections
    if answered:
        col_answer_given.insert_one(
            {
                'Question Intent': question_intent,
                'Bot answer': bot_answer,
                'Answer': answer
            }
        )
    else:
        col_answer_not_given.insert_one(
            {
                'Question Intent': question_intent,
                'Bot answer': bot_answer,
                'Answer': answer
            }
        )
