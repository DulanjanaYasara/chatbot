from data import EntityExtractor
from suzy import ask_suzy


def breaknplay_bot(question):
    """The questions are extracted into entities and they are fed to the bot"""
    extractor = EntityExtractor()
    question_phrases = extractor.extract(question)

    # Prints the answer only if the answer is different from the set of answers given by the bot
    tot_ans = []
    for q in question_phrases:
        ans = ask_suzy(q)[0]
        if ans not in tot_ans:
            tot_ans.append(ans)

    question_phrases = '\n'.join(question_phrases)
    tot_ans = '\n'.join(tot_ans)

    return question_phrases, tot_ans
