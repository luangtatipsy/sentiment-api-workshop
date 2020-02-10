import re
import html
import emoji
from pythainlp import word_tokenize

THAINUM = {'๐': '0','๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9'}

RE_TAG = re.compile(r"<[^>]+>")
RE_HTTP_WWW = re.compile(r"(?:\b\S{3,}:\/{1,}\S*)|(?:[wW]{2,}\.\S+)")
RE_EXT = re.compile(
    r"\w+\.(html|htm|shtm|shtml|cgi|php|php3|asp|aspx|cfm|cfml|jsp|png|gif|jpg|java|class|webp|mp3|mp4|mov|pl|do)(\?\S*)?\b",
    flags=re.IGNORECASE,
)
RE_MENTION = re.compile(r"(?:^|\s)@\S+")
RE_EMAIL = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
RE_LAUGH = re.compile(r'(?:\s|\D|\A)(5{2,}[46]*5*\+*)|\b(?:ha\s*){2,}|\u0E16{3,}|5{3,}(?!.\d)\b', flags=re.IGNORECASE)
RE_NUMBER = re.compile(r'\d+')
RE_HASHTAG = re.compile(r'(#[^\s]+)(?:\Z|\s)')
RE_EMOJI = emoji.get_emoji_regexp()


REPLACE_NUMBER = ' NUMBER '
REPLACE_LINK = ' LINK '
REPLACE_MENTION = ' MENTION '
REPLACE_EMAIL = ' EMAIL '
REPLACE_LAUGH = ' LAUGH '
REPLACE_NUMBER = ' NUMBER '
REPLACE_HASHTAG = ' HASHTAG '


def normalize_thai_number(text):
  for key, value in THAINUM.items():
    text = text.replace(key, value)
    
  return text

def normalize_number(text, place_holder=REPLACE_NUMBER):
  text = RE_NUMBER.sub(place_holder, text) 
    
  return text


def remove_markup_tag(text):
  text = RE_TAG.sub("", text)
  
  return text


def normalize_link(text, place_holder=REPLACE_LINK):
    text = RE_HTTP_WWW.sub(place_holder, text)  # http, https, mailto, www.
    text = RE_EXT.sub(place_holder, text)  # .html, php3, .jpg
    
    return text
  

def normalize_mention(text, place_holder=REPLACE_MENTION):
    text = RE_MENTION.sub(place_holder, text) # @mention
    
    return text
  

def normalize_email(text, place_holder=REPLACE_EMAIL):
    text = RE_EMAIL.sub(place_holder, text)  # mail@address.com
    
    return text


def normalize_laugh(text, place_holder=REPLACE_LAUGH):
    text = RE_LAUGH.sub(place_holder, text) # 5545+, hahaha, 555
    
    return text

def unescape_html(text):
  return html.unescape(text)


def normalize_emoji(text):
    text = re.sub(RE_EMOJI,r" \1 ", text).strip()
  
    return text
  

def extract_hashtag(text):
  hashtags = re.findall(RE_HASHTAG, text)
  
  return hashtags


def normalize_hashtag(text, place_holder=REPLACE_HASHTAG):
  text = RE_HASHTAG.sub(place_holder, text)
  
  return text


def replace_with_actual_hashtag(tokens, hashtags):
  indice = [index for index, token in enumerate(tokens) if token == "HASHTAG"]
  
  if len(indice) > 0:
    for index, hashtag in zip(indice, hashtags):
      tokens.insert(index, hashtag)
      tokens.remove('HASHTAG')
    
  return tokens


def tokenize(text, stopwords=None, punctuation=None):
  tokens = word_tokenize(text, engine='newmm')
  tokens = [token.strip() for token in tokens if token.strip() != '']
  
  if stopwords:
    tokens = [token for token in tokens if token not in stopwords]
    
  if punctuation:
    tokens = [token for token in tokens if all([character not in punctuation for character in list(token)])]
  
  return tokens


def _return_token(token):
  return token