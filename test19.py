import streamlit as st

"""
# ***Word Analytics***
This app enables you to download any data set with (.csv) files to analyze
the word count and see the most frequent and known words in the context
"""

# load dataset
import pandas as pd

# upload the data from the user --- by Majid
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
if  st.checkbox('Show dataset head'):
    st.write('dataset head')
    st.write(df)


"""
## Analytics Part
"""

# count frequencies using CountVectorizer
col1, col2 = st.columns([0.3, 0.7])

@st.cache_data
def countWordFrequencies():
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df)
    words = vectorizer.get_feature_names_out()
    frequencies = X.toarray().sum(axis=0)

    return words, frequencies


with st.spinner('Calculating frequencies...'):
    words, frequencies = countWordFrequencies()

    dfWords = pd.DataFrame({'word': words, 'frequency': frequencies})

col1.write(dfWords.sort_values('frequency', ascending=False).head())

# show cloud
import numpy as np
import matplotlib.pyplot as plt
#from wordcloud import wordcloud
import wordcloud

@st.cache_data
def generateCloud(frequencies):
    radius = 300
    x, y = np.ogrid[:2 * radius, :2 * radius]

    mask = (x - radius) ** 2 + (y - radius) ** 2 > (radius - 20) ** 2
    mask = 255 * mask.astype(int)

    wc = WordCloud(background_color="white", repeat=True, mask=mask)
    wc.generate_from_frequencies(frequencies)

    return wc

def showCloud(wc, col):
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.imshow(wc, interpolation="bilinear")
    col.pyplot(fig)

with st.spinner('Generating word cloud...'):
    wc = generateCloud(dict(zip(dfWords['word'], dfWords['frequency'])))
    showCloud(wc, col2)

"""
Cleaning the Data
"""

col1, col2 = st.columns([0.4, 0.6])

@st.cache_data
def countWordFrequenciesExcludeStopWords():
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df)
    words = vectorizer.get_feature_names_out()
    frequencies = X.toarray().sum(axis=0)
    return words, frequencies

with st.spinner('Calculating frequencies with stopwords...'):
    words, frequencies = countWordFrequenciesExcludeStopWords()
    dfWords = pd.DataFrame({'word': words, 'frequency': frequencies})

col1.write(dfWords.sort_values('frequency', ascending=False).head())

with st.spinner('Generating word cloud...'):
    wc = generateCloud(dict(zip(dfWords['word'], dfWords['frequency'])))
    showCloud(wc, col2)

"""
Interesting Words
"""

additional_stopwords = st.text_input('additional stop words (comma separated)', value="https")

n_grams = st.radio('number of grams',(1,2,3,4,5), horizontal=True)

@st.cache_data
def showCloudWithGrams(ngrams, additional_stopwords):
    from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
    custom_stop_words = list(ENGLISH_STOP_WORDS.union(additional_stopwords.split(',')))
    vectorizer = CountVectorizer(stop_words=custom_stop_words,ngram_range=(ngrams,ngrams))
    X = vectorizer.fit_transform(df['tweet_text'])
    words = vectorizer.get_feature_names_out()
    frequencies = X.toarray().sum(axis=0)

    dfWords = pd.DataFrame({'word': words, 'frequency': frequencies})

    wc = generateCloud(dict(zip(dfWords['word'], dfWords['frequency'])))
    showCloud(wc, st)

    st.write(dfWords.sort_values('frequency', ascending=False).head())

with st.spinner('Generating word cloud...'):
    showCloudWithGrams(n_grams, additional_stopwords)

"""
Finish
"""