from pymongo import MongoClient

client = MongoClient()

# Access database objects
db = client.answerComparison
col_answer_given = db.answered
col_answer_not_given = db.unanswered
col_q_not_given = db.notgiven
col_to_summarize = db.tosum


def remove_data():
    """Removes the data in all collections"""
    # Removing the existing data
    col_answer_given.remove()
    col_answer_not_given.remove()
    col_q_not_given.remove()
    col_to_summarize.remove()


def export_q_a(question, question_intent, answer, bot_answer, answered, has_to_summarize=False):
    """Exports the questions and answers to the database based on whether they are answered or has to be summarized"""
    # Insert document into collections
    if answered:
        col_answer_given.insert_one(
            {
                'Question Intent': question_intent,
                'Question': question,
                'Bot answer': bot_answer,
                'Answer': answer
            }
        )
    else:
        if has_to_summarize:
            col_to_summarize.insert_one(
                {
                    'Question Intent': question_intent,
                    'Question': question,
                    'Answer': answer
                }
            )
        else:
            col_answer_not_given.insert_one(
                {
                    'Question Intent': question_intent,
                    'Question': question,
                    'Bot answer': bot_answer,
                    'Answer': answer
                }
            )


def not_given_bot(question_intent, question, answer):
    """The questions that are not given to the bot is stored in separate collection"""
    col_q_not_given.insert_one(
        {

            'Question': question,
            'Question Intent': question_intent,
            'Answer': answer
        }
    )
