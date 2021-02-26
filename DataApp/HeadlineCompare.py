"""

    Author: Markus Hutnik
    Description: This is a simple web app that lets a user select a headline from a list
                 of headlines available in the database, and find other similar headlines.
                 Normally, I would have this connect straight to the database with pandas
                 read_sql(). For the purpose of turning this in, I just have it read the 
                 data from a csv.

"""

import streamlit as st
import pandas as pd
from textblob import TextBlob
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
from nltk.corpus import stopwords
import string
import pickle

no_selection = '--select--'

@st.cache
def load_data_and_model():
    """
    Load the data set and load the pickled dictionary of tags for headlines.
    This method gets cached because reloading the data often can hurt performance.

    Returns:
        DataFrame -- data from news_data.csv
        dict -- dictionary of document tags and full, uncleaned headlines
    """

    df = pd.read_csv('news_data.csv')
    with open('tag_lookup.pickle', 'rb') as f:
        tag_lookup = pickle.load(f)

    return df, tag_lookup

def get_selected_headline(df):
    """
    Creates a dropdown menu and gets the selected item from it.

    Arguments:
        df {DataFrame} -- all the news article data

    Returns:
        str -- headline selected from dropdown menu
    """

    headlines = [df['headline'][i] for i in range(len(df))]
    headlines.insert(0, no_selection)

    st.markdown('## Select a headline to see other similar headlines')
    selection = st.selectbox('', headlines)

    return selection

def clean_headline(headline):
    """
    Removes stop words and punctuation from a headline.

    Arguments:
        headline {str} -- heaadline to be cleaned

    Returns:
        list -- list of words in the headline, excluding stop words and punctuation
    """

    stop_words = set(stopwords.words('english'))
    return [word for word in nltk.word_tokenize(headline) if word not in stop_words and word not in string.punctuation]

def get_sentiment(headline):
    """
    Creates a TextBlob from a headline and find the sentiment.

    Arguments:
        headline {str} -- the selected headline from the drop

    Returns:
        TextBlob -- a TextBlob object made from the headline
        str -- the sentiment of the headline in plain english
    """
    
    blob = TextBlob(headline)

    if blob.sentiment.polarity > 0.01:
        sentiment = 'positive'
    elif blob.sentiment.polarity >= -0.01 and blob.sentiment.polarity <= 0.01:
        sentiment = 'neutral'
    else:
        sentiment = 'negative'
    
    return blob, sentiment

def main():
    st.title('Compare News Articles')
    df, tag_lookup = load_data_and_model()

    # load the model created from the 'compare_headline' notebook
    model = Doc2Vec.load('headline_model')
    headline = get_selected_headline(df)

    # if a headline was selected, show the top 5 most similar headlines and their sentiment
    if headline != no_selection:
        clean = clean_headline(headline)
        similar = model.docvecs.most_similar(positive=[model.infer_vector(clean)],topn=6)
        similar.pop(0)

        blob, sentiment = get_sentiment(headline)

        st.markdown(f'### Sentiment of selection: {sentiment}')
        st.write(f'Polarity: {round(blob.sentiment.polarity, 3)}')
        st.write(f'Subjectivity: {round(blob.sentiment.subjectivity, 3)}')
        st.write('')

        for i, s in enumerate(similar):
            st.markdown(f'#### {i}: {tag_lookup[s[0]]}')

            blob, sentiment = get_sentiment(tag_lookup[s[0]])

            st.write(f'Polarity: {round(blob.sentiment.polarity, 3)}')
            st.write(f'Subjectivity: {round(blob.sentiment.subjectivity, 3)}')
            # st.write('')

if __name__ == '__main__':
    main()