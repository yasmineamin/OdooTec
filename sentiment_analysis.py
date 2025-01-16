from fasttext import load_model
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from odoo import models, fields
import os

class SentimentAnalysis(models.Model):
    _name = 'sentiment.analysis'
    _description = 'Sentiment Analysis'

    ticket_description = fields.Text(string='Ticket Description')
    sentiment_result = fields.Char(string='Sentiment Result')

    def load_sentiment_model(self):
        """
        Load the FastText sentiment model.
        """
        model_path = os.path.join("C:/Users/Yasmine/odoo/Custom_modules/ticketing/data", 'fasttext_model_vader.bin')
        try:
            return load_model(model_path)
        except Exception as e:
            print(f"Error loading the sentiment model: {str(e)}")
            return None



    def action_analyze_sentiment(self):
        """
        Analyze the sentiment of the ticket description.
        """
        for record in self:
            description = record.ticket_description
            sentiment = self.analyze_sentiment(description)
            record.sentiment_result = sentiment

    def analyze_sentiment(self, description):
        """
        Perform sentiment analysis using FastText and VADER.
        """
        # Use VADER for fallback sentiment analysis
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(description)['compound']

        # Use FastText for more accurate sentiment classification
        model = self.load_sentiment_model()
        if model:
            prediction = model.predict(description, k=1)
            return prediction[0][0].replace('__label__', '')
        else:
            # Fallback to VADER analysis
            if sentiment_score > 0.05:
                return 'Positive'
            elif sentiment_score < -0.05:
                return 'Negative'
            else:
                return 'Neutral'

