
from odoo import models, fields, api
import os
from fasttext import load_model
import html2text


class Ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    # region Fields
    classification = fields.Text(
        string="Classification Result",
        readonly=True,
        default = "No Description Provided"
    )

    sentiment_analysis = fields.Selection(
        [
            ('positive', 'Positive'),
            ('negative', 'Negative'),
            ('neutral', 'Neutral'),
            ('no_description_provided', 'No Description Provided')
        ],
        string="Sentiment Analysis Result",
        default="no_description_provided"
    )

    # endregion

    # region Sentiment Analysis
    def load_sentiment_model(self):
        """Load FastText sentiment model from data directory"""
        model_path = os.path.join(
            "C:/Users/manar/odooprojects/Ticketing/custom_addons/Tickets/data",
            'sentiment_modelll.bin'
        )
        try:
            return load_model(model_path)
        except Exception as e:
            print(f"Error loading sentiment model: {str(e)}")
            print("The problem may be because you did not specify the ai model path in the file models/ticket.py")
            return None

    def analyze_sentiment(self, description):
        """Analyze ticket description sentiment"""
        if not description:
            return "No Description Provided"

        sanitized = html2text.html2text(description).strip().replace("\n", " ")
        model = self.load_sentiment_model()

        if not model:
            return "Model Not Loaded"

        try:
            prediction, _ = model.predict(sanitized, k=1)
            return prediction[0].replace("__label__", "") if prediction else "Unknown"
        except Exception as e:
            print(f"Sentiment analysis error: {str(e)}")
            return "Error"

    def action_analyze_sentiment(self):
        """Button handler for sentiment analysis"""
        for ticket in self:
            ticket.sentiment_analysis = (
                self.analyze_sentiment(ticket.description)
                if ticket.description
                else "no_description_provided"
            )

    # endregion

    # region Ticket Classification
    def load_ticketing_model(self):
        """Load FastText classification model from data directory"""
        model_path = os.path.join(
            "C:/Users/manar/odooprojects/Ticketing/custom_addons/Tickets/data",
            'fasttext_category_classifier.bin'
        )
        try:
            return load_model(model_path)
        except Exception as e:
            print(f"Error loading classification model: {str(e)}")
            print("The problem may be because you did not specify the ai model path in the file models/ticket.py")
            return None

    def classify_ticket(self, description):
        """Classify ticket description"""
        if not description:
            return "No Description Provided"

        sanitized = str(description).strip().replace("\n", " ")
        model = self.load_ticketing_model()

        if not model:
            return "Model Not Loaded"

        try:
            prediction = model.predict(sanitized, k=1)
            return prediction[0][0].replace("__label__", "") if prediction else "Unknown"
        except Exception as e:
            print(f"Classification error: {str(e)}")
            return "Error"

    def action_classify_ticket(self):
        """Button handler for ticket classification"""
        for ticket in self:
            ticket.classification = (
                self.classify_ticket(ticket.description)
                if ticket.description
                else "No Description Provided"
            )

    # endregion

    # region CRUD Overrides
    @api.model_create_multi
    def create(self, vals_list):
        """Auto-classify on ticket creation"""
        tickets = super().create(vals_list)
        for ticket in tickets:
            if ticket.description:
                ticket.classification = self.classify_ticket(ticket.description)
                ticket.sentiment_analysis = self.analyze_sentiment(ticket.description)
        return tickets

    def write(self, vals):
        """Auto-classify on description update"""
        res = super().write(vals)
        if 'description' in vals:
            for ticket in self:
                ticket.classification = self.classify_ticket(ticket.description)
                ticket.sentiment_analysis = self.analyze_sentiment(ticket.description)
        return res
    # endregion