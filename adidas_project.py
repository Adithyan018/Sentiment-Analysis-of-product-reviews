# -*- coding: utf-8 -*-
"""adidas Project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e2JNbE9jiLfnTCiERj8w6LYIpbWBIJDv
"""

import pandas as pd
import numpy as np
import re
import string
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

df= pd.read_csv('/content/adidas_data_15-09-2023 (1).csv')
df.head(10)

df.columns

df.isnull().sum()

df.dropna(inplace=True)
df.isnull().sum()

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

df['cleaned_review'] = df['Reviews'].apply(preprocess_text)

df['review_length'] = df['cleaned_review'].apply(lambda x: len(str(x).split()))

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='sentiment', palette='Set2')
plt.title('Distribution of Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.show()

plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='Price', bins=20, kde=True)
plt.title('Distribution of Product Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

import pandas as pd
top_topics = df['ReviewTopic'].value_counts().head(10)
plt.figure(figsize=(10, 6))
top_topics.plot(kind='bar', color='skyblue')
plt.title('Top 10 Review Topics')
plt.xlabel('Review Topic')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=45, ha='right')
plt.show()

plt.figure(figsize=(6, 6))
df['VerifiedPurchaser'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
plt.title('Percentage of Verified vs. Non-Verified Purchases')
plt.ylabel('')
plt.show()

from textblob import TextBlob
!pip install textblob
df['polarity'] = df['cleaned_review'].apply(lambda x: TextBlob(x).sentiment.polarity)
df['sentiment'] = df['polarity'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))

print(classification_report(y_test, y_pred))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

for sentiment in ['positive', 'negative', 'neutral']:
    text = ' '.join(df[df['sentiment'] == sentiment]['cleaned_review'])
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"WordCloud for {sentiment.capitalize()} Reviews")
    plt.show()

from textblob import TextBlob

review = input("input: ")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@w+|\#', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

cleaned = clean_text(review)

blob = TextBlob(cleaned)
polarity = blob.sentiment.polarity

if polarity > 0:
    sentiment = "Positive"
elif polarity < 0:
    sentiment = "Negative"
else:
    sentiment = "Neutral"

print(f"Review: {review}")
print(f"Polarity Score: {polarity}")
print(f"Predicted Sentiment: {sentiment}")

