import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from nltk import tokenize


class ColumnSelectorExtractor(BaseEstimator, TransformerMixin):
    """
    Class for building sklearn Pipeline step.
    This class should be used to select a column from a pandas data frame.
    """

    def __init__(self, column):
        if isinstance(column, str):
            self.column = column
        else:
            raise ValueError('Invalid type for column')

    def fit(self, x, y=None):
        return self

    def transform(self, data_frame):
        return data_frame[self.column]

    def get_feature_names(self):
        return [self.column]


class SubjectAndBodyMergerExtractor(BaseEstimator, TransformerMixin):
    """
    Class for building sklearn Pipeline step.
    This class should be used to select a column from a pandas data frame.
    """

    def fit(self, x, y=None):
        return self

    def transform(self, data_frame):
        return data_frame['subject'] + ' ' + data_frame['body']

    def get_feature_names(self):
        return ['subject_and_body']


class SimpleFeaturesExtractor(BaseEstimator, TransformerMixin):
    """
    Extract attributes given a list of tuples(name, callable)
    """

    def __init__(self, extractors_tuple=[]):
        self.names, self.extractors = zip(*extractors_tuple)

    def fit(self, x, y=None):
        return self

    def transform(self, mails):
        features = pd.DataFrame()
        for name, extractor in zip(self.names, self.extractors):
            features[name] = extractor(mails)

        return features

    def get_feature_names(self):
        return self.names

    def get_params(self, deep=False):
        return {'extractors_tuple': zip(self.names, self.extractors)}


def subject_length(mails):
    """Returns the subject length"""
    return mails.subject.map(lambda mail_subject: len(mail_subject))


def subject_spaces(mails):
    """Returns the number of blank spaces in the email subject normalized by the length of it"""
    return mails.subject.map(lambda mail_subject: float(mail_subject.count(' ')) / float(len(mail_subject)) if len(mail_subject) > 0 else 0)


def subject_caps(mails):
    """Returns the number of uppercase characters in the email subject normalized by the length of it"""
    return mails.subject.map(lambda mail_subject: sum(1.0 for c in mail_subject if c.isupper()) / float(len(mail_subject)) if len(mail_subject) > 0 else 0)


def body_length(mails):
    """Returns the body length"""
    return mails.body.map(lambda mail_body: len(mail_body))


def body_spaces(mails):
    """Returns the number of blank spaces in the email body normalized by the length of it"""
    return mails.body.map(lambda mail_body: float(mail_body.count(' ')) / float(len(mail_body)) if len(mail_body) > 0 else 0)


def body_caps(mails):
    """Returns the number of uppercase characters in the email body normalized by the length of it"""
    return mails.body.map(lambda mail_body: sum(1.0 for c in mail_body if c.isupper()) / float(len(mail_body)) if len(mail_body) > 0 else 0)


def body_sentences(mails):
    """Returns the number of sentences in the mail body"""
    return mails.body.map(lambda mail_body: len(tokenize.sent_tokenize(mail_body)))


def has_html(mails):
    """Returns 1 if the mail has a HTML content type and 0 if not"""
    return have_content_type(mails, 'html')


def has_image(mails):
    """Returns 1 if the mail has a image content type and 0 if not"""
    return have_content_type(mails, 'image')


def have_content_type(mails, content_type):
    """
    Returns true if any of the mails content types is equal to content_type
    """
    return mails.content_types.map(lambda mail_content_types: int(any([content_type in mct for mct in mail_content_types])))
