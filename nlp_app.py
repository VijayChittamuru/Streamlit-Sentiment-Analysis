import streamlit as st
from textblob import TextBlob
from nltk.stem.wordnet import WordNetLemmatizer
import re
import nltk


try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    print("Downloading necessary nltk data")
    nltk.download('wordnet')
except Exception as e:
    st.error("An unexpected error occurred")

# Taken from assignment guidelines
def clean_text(text):
    #Keeping only Text and digits
    text = re.sub(r"[^A-Za-z0-9]", " ", text)
    #Removes Whitespaces
    text = re.sub(r"\'s", " ", text)
    # Removing Links if any
    text = re.sub(r"http\S+", " link ", text)
    # Removes Punctuations and Numbers
    text = re.sub(r"\b\d+(?:\.\d+)?\s+", "", text)
    # Splitting Text
    text = text.split()
    # Lemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in text]
    text = " ".join(lemmatized_words)

    return text

# Streamlit GUI
st.title("Sentiment Analysis")

user_input = st.text_area("Enter the text you would like to analyze", height=100)

if(st.button("Analyze")):
    if(user_input):
        cleaned_input = clean_text(user_input)

        blob = TextBlob(cleaned_input)
        sentiment_score = blob.sentiment.polarity
        result = sentiment_score

        if result > 0: # Positive sentiment
            custom_emoji = ':blush:'
            st.success('Happy {}'.format(custom_emoji))
        elif result < 0: # Negative sentiment
            custom_emoji = ':disappointed:'
            st.warning('Sad {}'.format(custom_emoji))
        else: # Neutral sentiment
            custom_emoji = ':confused:'
            st.info('Neutral {}'.format(custom_emoji))
        st.success("Polarity Score is: {}".format(result))

    else:
        st.warning("Please enter some text to analyze")