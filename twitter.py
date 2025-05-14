mport dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import re
import os
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import base64
from io import BytesIO

# Register page
dash.register_page(__name__, path="/twitter", name="Twitter Trends")

# Load CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
twitter_path = os.path.join(BASE_DIR, "data", "tweets.csv")
df = pd.read_csv(twitter_path)

# Pick main text column
text_col = "tweet_full_text" if "tweet_full_text" in df.columns else None
if not text_col:
    layout = html.Div([html.H3("⚠️ No tweet text column found in dataset.")])
else:
    # === HASHTAGS ===
    def extract_hashtags(text):
        return re.findall(r"#\w+", str(text).lower())
    
    df['hashtags'] = df[text_col].apply(extract_hashtags)
    all_hashtags = [tag for sublist in df['hashtags'] for tag in sublist]
    hashtag_counts = Counter(all_hashtags)
    top_hashtags = pd.DataFrame(hashtag_counts.items(), columns=['hashtag', 'count']) \
        .sort_values(by='count', ascending=False).head(20)
    
    hashtag_fig = px.bar(
        top_hashtags, x='count', y='hashtag', orientation='h',
        title='📢 Top 20 Healthcare Hashtags on Twitter',
        labels={'count': 'Mentions', 'hashtag': 'Hashtag'},
        height=500
    )
    hashtag_fig.update_layout(margin=dict(t=50, l=100, r=40, b=40))

    # === WORD CLOUD ===
    stopwords = set(STOPWORDS)
    text_for_cloud = " ".join(df[text_col].dropna().astype(str).tolist()).lower()
    wordcloud = WordCloud(
        width=800, height=400,
        stopwords=stopwords,
        background_color='white',
        colormap='viridis'
    ).generate(text_for_cloud)

    # Convert wordcloud to image for Dash
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    encoded_image = base64.b64encode(buffer.getvalue()).decode()

    # === SENTIMENT ANALYSIS ===
    def get_sentiment(text):
        polarity = TextBlob(str(text)).sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"

    df['sentiment'] = df[text_col].apply(get_sentiment)
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']

    sentiment_fig = px.pie(
        sentiment_counts, names='Sentiment', values='Count',
        title="😊 Overall Tweet Sentiment", color='Sentiment',
        color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"}
    )

    # === Layout ===
    layout = html.Div([
        html.H2("🐦 Twitter Trends Related to the NHS", className='my-4'),

        html.H4("📢 Most Frequent Hashtags"),
        html.P("This chart shows the top hashtags related to NHS topics."),
        dcc.Graph(figure=hashtag_fig),

        html.H4("☁️ Word Cloud of Tweet Content"),
        html.P("Frequent non-hashtag words in tweets mentioning the NHS."),
        html.Img(src=f"data:image/png;base64,{encoded_image}", style={"width": "100%", "maxWidth": "800px"}),

        html.H4("😊 Sentiment Distribution"),
        html.P("Basic sentiment analysis using TextBlob."),
        dcc.Graph(figure=sentiment_fig)
    ])

