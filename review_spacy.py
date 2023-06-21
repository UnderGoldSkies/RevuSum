#install
#!pip install -U spacy
#!python -m spacy download en_core_web_sm

#Import the necessary library
import pandas as pd
import spacy
from space.lang.en.stop_words import STOP_WORDS
import string
from collections import Counter
from heapq import nlargest
import os


class Review_Spacy:

    def load_data(self):
        #pull the data
        url = os.getcwd() + '/raw_data/hotel_reviews.csv'
        self.raw_df = pd.read_csv(url)

    def combine_reviews(self):
        self.review_df = pd.DataFrame(pd.concat((
            self.raw_df['Negative_Review'], self.raw_df['Positive_Review']), axis=0),
                                      columns=['reviews'])

    def convert_review_to_str(self):
        self.reviews_str = self.review_df['reviews'].head(20).str.cat(sep=' ')

    def create_spacy(self):
        spacy_model = spacy.load('en_core_web_sm')
        self.doc = spacy_model(self.reviews_str)

    def cleaning(self):
        #cleaning
        self.keyword = []
        stopwords = list(STOP_WORDS)
        post_tag = ['PROPN', 'ADJ', 'VERB', 'NOUN']
        for token in self.doc:
            if token.text in stopwords or token.text in string.punctuation:
                continue
            if token.pos_ in post_tag:
                self.keyword.append(token.text)

    def freq_keyword(self):
        self.freq_keyword = Counter(self.keyword)
        max_freq = self.freq_keyword.most_common(5)[0][1]
        for word in self.freq_keyword.keys():
            self.freq_keyword[word] = self.freq_keyword[word]/max_freq

    def process_docs(self):
        self.sent_strength = {}
        for sent in self.doc.sents:
            for word in sent:
                if word.text in self.freq_keyword.keys():
                    if sent in self.sent_strength.keys():
                        self.sent_strength[sent] += self.freq_keyword[word.text]
                    else:
                        self.sent_strength[sent] = self.freq_keyword[word.text]

    def process_summary(self):
        summarized_sentences = nlargest(3, self.sent_strength, key=self.sent_strength.get)
        final_sentences = [w.text for w in summarized_sentences]
        summary = ' '.join(final_sentences)
        return summary
