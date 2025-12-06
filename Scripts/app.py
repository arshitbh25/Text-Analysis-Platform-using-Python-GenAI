import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from matplotlib.pyplot import xlabel

from text_cleaner import clean_text, lemmatize_spacy
from nlp_functions import show_wordcloud, plot_top_ngram_bar_chart, emotion_detection, sentiment_detection, classify_customs, summarize_large_texts

st.title("INTERACTIVE TEXT ANALYSIS PLATFORM")
st.divider()

a = st.sidebar.radio("SELECT ONE :- ",["Process Textual Data","Process CSV file"])

# For Textual data :
if a=="Process Textual Data":
    st.header("Input your Textual Data")
    text = st.text_area("Enter your Text", height=150)

    if st.button("Analyze"):
        st.divider()
        if not text.strip():
            st.warning("Please enter your text!")
        else:
            # Cleaning and Processing data
            cleaned = clean_text(text)
            tokens = lemmatize_spacy(cleaned)

            # Word Cloud
            if tokens:
                st.subheader("Word Cloud")
                joined_tokens = " ".join(tokens)
                wc_plot = show_wordcloud(joined_tokens)
                st.pyplot(wc_plot)
            st.divider()

            # n-gram analysis
            st.subheader("N-Gram Analysis")
            plot_top_ngram_bar_chart(tokens,gram_n=2)
            st.divider()

            # Emotion Detection
            st.subheader("Emotion Detection")
            top_emotion_df = emotion_detection(text)
            max_index = top_emotion_df["Score"].idxmax()
            Emotion = top_emotion_df.loc[max_index, "Emotion"]
            Score = top_emotion_df.loc[max_index, "Score"]
            st.write(f"Predicted Emotion :- {Emotion.title()}, with {Score * 100}% confidence")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Top 5 Emotions :-")
                st.dataframe(top_emotion_df)
            with col2:
                st.markdown("Visualizing through Bar Chart :-")
                fig = px.bar(top_emotion_df, x="Emotion", y="Score", color="Emotion")
                fig.update_layout(
                    template = 'plotly_white',
                    height = 290 # It is important to fix the height of plot, to match the table
                )
                st.plotly_chart(fig)
            st.divider()

            # Sentimental Analysis
            st.subheader("Sentiment Detection")
            result = sentiment_detection(text)
            if "error" in result:
                st.write(f"Error: {result["error"]}")
            else:
                st.write(f"Overall Sentiment :- {result["Overall_sentiment"]}, with score {max(result["Average_score"].values())}")
                df = pd.DataFrame(result["Average_score"].items(), columns=["Sentiment", "Score"])
                st.dataframe(df)
                st.divider()

            # Tone of speech detection
            st.subheader("Tone of Speech Detection")
            output = classify_customs(text)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"Predicted : {output["Predicted_Category"]}, Score : {output["Score"]}")
                st.write("Other Top Predicted Categories :-")
                for label, score in output["All_Categories"][1:6]:
                    st.write(f"Label : {label}, Score : {score}")
            with col2:
                labels=[]
                scores=[]
                for label, score in output["All_Categories"][1:6]:
                    labels.append(label)
                    scores.append(score)
                # Ploting graph
                fig = px.bar(x=labels, y=scores, color=labels, title="Other top 5 predicted category",
                             labels={"Value":"Value Count"},
                             height=400)
                fig.update_layout(xaxis=dict(title="Labels"),yaxis=dict(title="Score"))
                st.plotly_chart(fig)
            st.divider()

            # Summary Generation
            st.subheader("Summary Generation")
            summary = summarize_large_texts(text)
            st.write(summary)


# For CSV file
if a=="Process CSV file":
    st.header("Upload your CSV file")
    uploaded_file = st.file_uploader("Choose an CSV file",type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.divider()

        st.header("Choose filtering option")

        # User selecting column to filter data
        column_name = st.selectbox("Select the column on which basis you want to filter the table", df.columns)

        # Selecting unique values
        unique_vals = df[column_name].dropna().unique()
        selected_value = st.multiselect(f"Please choose value from {column_name}", unique_vals)

        # Select the textual column
        text_processing_column = st.selectbox("Select column for text analysis ", df.columns)
        filtered_df = df[df[column_name].isin(selected_value)]
        filtered_df = filtered_df[text_processing_column]
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)
        # text = " ".join(filtered_df.drop().astype(str))
        text = " ".join(filtered_df.astype(str).tolist())

        if st.button("Analyze"):
            st.divider()

            # Cleaning and Processing data
            cleaned = clean_text(text)
            tokens = lemmatize_spacy(cleaned)

            # Word Cloud
            if tokens:
                st.subheader("Word Cloud")
                joined_tokens = " ".join(tokens)
                wc_plot = show_wordcloud(joined_tokens)
                st.pyplot(wc_plot)
            st.divider()

            # n-gram analysis
            st.subheader("N-Gram Analysis")
            plot_top_ngram_bar_chart(tokens, gram_n=2)
            st.divider()

            # Emotion Detection
            st.subheader("Emotion Detection")
            top_emotion_df = emotion_detection(text)
            max_index = top_emotion_df["Score"].idxmax()
            Emotion = top_emotion_df.loc[max_index, "Emotion"]
            Score = top_emotion_df.loc[max_index, "Score"]
            st.write(f"Predicted Emotion :- {Emotion.title()}, with {Score * 100}% confidence")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Top 5 Emotions :-")
                st.dataframe(top_emotion_df)
            with col2:
                st.markdown("Visualizing through Bar Chart :-")
                fig = px.bar(top_emotion_df, x="Emotion", y="Score", color="Emotion")
                fig.update_layout(
                    template='plotly_white',
                    height=290  # It is important to fix the height of plot, to match the table
                )
                st.plotly_chart(fig)
            st.divider()

            # Sentimental Analysis
            st.subheader("Sentiment Detection")
            result = sentiment_detection(text)
            if "error" in result:
                st.write(f"Error: {result["error"]}")
            else:
                st.write(
                    f"Overall Sentiment :- {result["Overall_sentiment"]}, with score {max(result["Average_score"].values())}")
                df = pd.DataFrame(result["Average_score"].items(), columns=["Sentiment", "Score"])
                st.dataframe(df)
                st.divider()

            # Tone of speech detection
            st.subheader("Tone of Speech Detection")
            output = classify_customs(text)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"Predicted : {output["Predicted_Category"]}, Score : {output["Score"]}")
                st.write("Other Top Predicted Categories :-")
                for label, score in output["All_Categories"][1:6]:
                    st.write(f"Label : {label}, Score : {score}")
            with col2:
                labels = []
                scores = []
                for label, score in output["All_Categories"][1:6]:
                    labels.append(label)
                    scores.append(score)
                # Ploting graph
                fig = px.bar(x=labels, y=scores, color=labels, title="Other top 5 predicted category",
                             labels={"Value": "Value Count"},
                             height=400)
                fig.update_layout(xaxis=dict(title="Labels"), yaxis=dict(title="Score"))
                st.plotly_chart(fig)