import string
import threading
import streamlit as st
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
import pickle
import re



# Initialize the recognizer
recognizer = sr.Recognizer()

# Load the TfidfVectorizer
with open('C:/Users/User/Desktop/payhack2024/Speech-to-Text-Converter/tfidf_vectorizer.pkl', 'rb') as file:
    loaded_vectorizer = pickle.load(file)

# Load the Naive Bayes model
with open('C:/Users/User/Desktop/payhack2024/Speech-to-Text-Converter/naive_bayes_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Function to capture and process live microphone input
def listen_microphone(text_placeholder, detection_placeholder):
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        while st.session_state.is_listening:
            try:
                # Capture audio from the microphone
                audio = recognizer.listen(source, timeout=50, phrase_time_limit=50)
                # Convert speech to text
                text = recognizer.recognize_google(audio)

                # Display the transcription
                text_placeholder.markdown(
                    f"<div class='box'><b>Speech-to-Text:</b><br>{text}</div>",
                    unsafe_allow_html=True,
                )

                # Preprocess and predict
                text = preprocess_test(text)
                sentence_tfidf = loaded_vectorizer.transform([text])
                predicted_label = loaded_model.predict(sentence_tfidf)

                # Display the prediction
                if predicted_label[0] == 1:
                    detection_placeholder.markdown(
                        "<div class='scam-box'><b>Detection:</b><br>This Call is detected to be <span class='scam'>SCAM</span></div>",
                        unsafe_allow_html=True,
                    )
                elif predicted_label[0] == 0:
                    detection_placeholder.markdown(
                        "<div class='not-scam-box'><b>Detection:</b><br>This Call is detected to be <span class='not-scam'>NOT A SCAM</span></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    detection_placeholder.markdown(
                        "<div class='box'><b>Detection:</b><br>Unexpected label detected.</div>",
                        unsafe_allow_html=True,
                    )

            except sr.UnknownValueError:
                text_placeholder.markdown(
                    "<div class='box'>Listening... (could not understand audio)</div>",
                    unsafe_allow_html=True,
                )
            except sr.RequestError as e:
                text_placeholder.markdown(
                    f"<div class='box'>API Error: {e}</div>", unsafe_allow_html=True
                )
            except Exception as e:
                text_placeholder.markdown(
                    f"<div class='box'>Error: {e}</div>", unsafe_allow_html=True
                )

def preprocess_test(text):
    preprocessed_sentence = clean_text(text)
    preprocessed_sentence = remove_stopwords(preprocessed_sentence)
    preprocessed_sentence = stemm_text(preprocessed_sentence)
    return text

def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    print(text)
    return text

def remove_stopwords(text):
    stop_words = stopwords.words('english')
    more_stopwords = ['u', 'im', 'c']
    stop_words = stop_words + more_stopwords
    text = ' '.join(word for word in text.split(' ') if word not in stop_words)
    print(text)

    return text

def stemm_text(text):
    stemmer = nltk.SnowballStemmer("english")
    text = ' '.join(stemmer.stem(word) for word in text.split(' '))
    print(text)

    return text

# Main Streamlit application
def main():
    # CSS for UI Styling
    st.markdown(
        """
        <style>
        .button-container {
            display: flex;
            justify-content: flex-start;
            gap: 10px;
            margin-top: 20px;
        }
        .button {
            padding: 10px 20px;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 14px;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .box {
            margin-top: 10px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
            font-size: 14px;
        }
        .scam-box {
            color: white;
            background-color: red;
            margin-top: 10px;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        .not-scam-box {
            color: white;
            background-color: green;
            margin-top: 10px;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
      
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True, height=500):

        st.title(":orange[_S C A M_] :sunglasses:")
        st.header(":orange[_S_]:green[_cam_] :orange[_C_]:green[_all_] :orange[_A_]:green[_nalysis_] :orange[_M_]:green[_onitoring_]", divider="gray")

        # Initialize session state for controlling start/stop
        if 'is_listening' not in st.session_state:
            st.session_state.is_listening = False

        # Placeholder for dynamic text updates
        text_placeholder = st.empty()
        detection_placeholder = st.empty()

        # Start and Stop Buttons
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Start", key="start_button"):
                st.session_state.is_listening = True
                listen_microphone(text_placeholder, detection_placeholder)

        with col2:
            if st.button("Stop", key="stop_button"):
                st.session_state.is_listening = False
                st.write("Stopped listening.")


if __name__ == "__main__":
    main()



