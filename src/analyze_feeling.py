from textblob import TextBlob


def get_subj(text):
    return TextBlob(text).sentiment.subjectivity


def get_pola(text):
    return TextBlob(text).sentiment.polarity


def analyze(score):
    if score < 0:
        return 'Negativo'
    elif score == 0:
        return 'Neutro'
    else:
        return 'Positivo'