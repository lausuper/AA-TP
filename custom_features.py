import email
from nltk import tokenize
from sklearn.base import BaseEstimator, TransformerMixin
import email_text_retrieval as er
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentsStats(BaseEstimator, TransformerMixin):
  def fit(self, x, y = None):
    return self

  def transform(self, message_body):
    sid = SentimentIntensityAnalyzer()
    body_sentences = tokenize.sent_tokenize(message_body)
    sentences_stats = map(lambda sentence: sid.polarity_scores(sentence), body_sentences)
    stats = { 'neg' : 0, 'neu' : 0, 'pos' : 0 }
    for sentence_stat in sentences_stats:
      stats['neg'] += sentence_stat['neg']
      stats['neu'] += sentence_stat['neu']
      stats['pos'] += sentence_stat['pos']

    stats['neg'] /= len(sentences_stats)
    stats['neu'] /= len(sentences_stats)
    stats['pos'] /= len(sentences_stats)

    return stats

class EmailParser(BaseEstimator, TransformerMixin):
  def fit(self, x, y = None):
    return self

  def transform(self, emails):
    return map(lambda message: email.message_from_string(message.encode('ascii', 'ignore')), emails)

class ItemSelector(BaseEstimator, TransformerMixin):
  def __init__(self, key):
    self.key = key

  def fit(self, x, y=None):
    return self

  def transform(self, messages):
    if self.key == 'subject':
      return map(lambda message: message.get('subject'), messages)
    else:
      return map(lambda message: er.retrieve_payload_text(message), messages)