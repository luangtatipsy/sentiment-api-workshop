from preprocess import normalize_thai_number, normalize_number, remove_markup_tag, normalize_link, normalize_mention 
from preprocess import normalize_email, normalize_laugh, unescape_html, normalize_emoji, extract_hashtag
from preprocess import normalize_hashtag, replace_with_actual_hashtag, tokenize, _return_token

import pickle
from pythainlp.corpus import thai_stopwords
from string import punctuation

stopwords = thai_stopwords()
punctuation += '“” ️'

filename = 'models/tfidf_lr.pkl'
pipeline = pickle.load(open(filename, 'rb'))

def transform(text):
    text = text.lower()
    text = normalize_thai_number(text)
    text = unescape_html(text)
    text = remove_markup_tag(text)
    text = normalize_link(text)
    text = normalize_mention(text)
    text = normalize_email(text)
    text = normalize_laugh(text)
    text = normalize_number(text, place_holder='')
    text = normalize_emoji(text)
    hashtags = extract_hashtag(text)
    text = normalize_hashtag(text, place_holder='')
    tokens = tokenize(text, stopwords=None, punctuation=punctuation)
    tokens = replace_with_actual_hashtag(tokens, hashtags)
    
    return tokens


def get_sentiment_result(text):
    tokens = transform(text)
    label = pipeline.predict([tokens])[0]
    predicted_prob = pipeline.predict_proba([text])
    confidence = float(max(predicted_prob[0]))

    print(label, confidence, flush=True)

    return label, round(confidence, 3)