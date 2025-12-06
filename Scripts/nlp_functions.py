# Word Cloud
import streamlit
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
def show_wordcloud(text):
    try:
        word_cloud = WordCloud(width=800,height=400,background_color="white").generate(text)
        fig = plt.figure(figsize=(10,5))
        plt.imshow(word_cloud)
        plt.axis("off")
        return fig
    except Exception as e:
        return f"Error generating word cloud:m {e}"

# n-gram
from nltk.util import ngrams
from collections import Counter
import plotly.graph_objects as go

def plot_top_ngram_bar_chart(tokens, gram_n=2, top_n=15):
    try:
        n_grams = list(ngrams(tokens, gram_n))
        # Counter(n_grams)
        ngram_counts = Counter(n_grams).most_common(top_n)

        if not ngram_counts:
            raise ValueError("No n-grams found in the given token list")

        labels = []
        counts = []
        for biagram, count in ngram_counts:
            labels.append(" ".join(biagram))
            counts.append(count)

        # Generating bar-graph
        fig = go.Figure(
            data=[
                go.Bar(
                    x=labels,
                    y=counts,
                    text=counts,
                    textposition="outside"
                )
            ]
        )

        fig.update_layout(
            height=550,
            title="Top 15 Biagrams",
            xaxis_title="Labels",
            yaxis_title="Frequency"
        )

        st.plotly_chart(fig)

    except Exception as e:
        return f"An Error occured while n-gram analysis: {e}"

# Creating Chunks
import spacy

def split_into_chunks(text, max_length=500):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    chunks = []
    current_chunk = ""

    for sent in doc.sents:
        sentence = sent.text.strip()
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Emotion analysis
from transformers import pipeline
import plotly.express as px
import pandas as pd
from collections import defaultdict

model_name = "nateraw/bert-base-uncased-emotion"

emotion_classifier = pipeline("text-classification", model=model_name, tokenizer=model_name, top_k=None)

def emotion_detection(text):
    chunks = split_into_chunks(text)
    emotion_total = {}
    emotion_count = {}
    emotion_count = defaultdict(int)

    for chunk in chunks:
        results = emotion_classifier(chunk)[0]
        for result in results:
            label = result["label"]
            score = result["score"]
            emotion_total[label] = emotion_total.get(label, 0) + score
            emotion_count[label] += 1

    emotion_count = dict(emotion_count)

    emotion_average = {label: emotion_total[label] / emotion_count[label] for label in emotion_total}
    sorted_emotion = sorted(emotion_average.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_emotion[:5]
    df = pd.DataFrame(top_5, columns=["Emotion", "Score"])

    return df

# Sentiment Analysis

model_name = "cardiffnlp/twitter-roberta-base-sentiment"

sentiment_classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name, return_all_scores=True)

def sentiment_detection(text):
    try:
        sentiment_labels = {
            "LABEL_0": "Negative",
            "LABEL_1": "Neutral",
            "LABEL_2": "Positive"
        }
        chunks = split_into_chunks(text)
        score_total = {"Negative": 0.0, "Neutral": 0.0, "Positive": 0.0}
        chunk_count = len(chunks)

        for chunk in chunks:
            results = sentiment_classifier(chunk)[0]
            for res in results:
                label = sentiment_labels[res["label"]]
                score_total[label] += res["score"]

        avg_score = {}
        for label in score_total:
            avg_score[label] = score_total[label] / chunk_count

        overall_sentiment = max(avg_score, key=avg_score.get)

        return {
            "Overall_sentiment": overall_sentiment,
            "Average_score": avg_score
        }

    except Exception as e:
        print(f"error {e}")

# Tone of speech classification

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = ["factual","opinion","question","command","emotion","personal experience","suggestion","story","prediction","warning","instruction","definition","narrative","news","argument"]


def chunk_text(sentences, chunk_size=5, overlap=2):
    chunks = []
    start = 0
    while start < len(sentences):
        end = start + chunk_size
        chunk = sentences[start:end]
        chunks.append(" ".join(chunk))

        if end >= len(sentences):
            break

        start += chunk_size - overlap
    return chunks

def classify_customs(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    if len(sentences) <= 5:
        result = classifier(text, candidate_labels=labels)
        return {
            "Text": text,
            "Predicted_Category": result["labels"][0],
            "Score": result["scores"][0],
            "All_Categories": list(zip(result["labels"], result["scores"]))
        }
    else:
        chunks = chunk_text(sentences)

        # Calculate aggregated score:
        aggregated_scores = {label: 0.0 for label in labels}
        for chunk in chunks:
            result = classifier(chunk, candidate_labels=labels)
            for label, score in zip(result["labels"], result["scores"]):
                aggregated_scores[label] += score

        # Calculate average score:
        chunks_count = len(chunks)
        average_scores = {label: score / chunks_count for label, score in aggregated_scores.items()}

        # Sorted score
        sorted_category = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)

        return {
            "text": text,
            "Predicted_Category": sorted_category[0][0],
            "Score": sorted_category[0][1],
            "All_Categories": sorted_category
        }

# Text Summarization

def summarize_large_texts(text):
    summarizer = pipeline("summarization",model="facebook/bart-large-cnn")
    chunks = split_into_chunks(text,max_length=500)

    chunk_summaries = []
    for chunk in chunks:
        input_length = len(chunk.split())
        max_summary_len = int(input_length*0.7)
        min_summary_len = int(input_length*0.3)
        summary = summarizer(text, max_length=max_summary_len, min_length=min_summary_len, do_sample=False)[0]["summary_text"]
        chunk_summaries.append(summary)

    combined_summary_text = " ".join(chunk_summaries)

    input_length = len(combined_summary_text.split())
    max_summary_len = int(input_length*0.9)
    min_summary_len = int(input_length*0.3)
    final_summary = summarizer(combined_summary_text, max_length=max_summary_len, min_length=min_summary_len, do_sample=False)[0]["summary_text"]

    return final_summary