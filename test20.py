import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from collections import Counter
import string

# Function to preprocess text
def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Convert to lowercase
    text = text.lower()
    return text

# Function to plot word frequency
def plot_word_frequency(text):
    # Tokenize and preprocess text
    words = preprocess_text(text).split()
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    
    # Calculate word frequency
    word_freq = Counter(words)
    
    # Create a DataFrame for visualization
    word_freq_df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
    
    # Sort DataFrame by frequency
    word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)
    
    # Display the table
    st.table(word_freq_df)
    
    # Plot word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    st.image(wordcloud.to_array(), use_container_width=True)
    
    # Plot bar chart
    st.bar_chart(word_freq_df.set_index('Word'))

# Streamlit app
def main():
    st.title("Word Frequency Analyzer")
    
    # Input text area
    text = st.text_area("Enter text for analysis:", "Type or paste your text here...")
    
    # Analyze button
    if st.button("Analyze"):
        plot_word_frequency(text)

# Run the app
if __name__ == "__main__":
    main()
