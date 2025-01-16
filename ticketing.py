import os

from fasttext import load_model

from odoo import models, fields


class Ticketing(models.Model):
    _name = 'ticketing.model'
    _description = 'Ticketing Class Model'

    ticket_name = fields.Char(string='Ticket Name')
    ticket_description = fields.Text(string='Ticket Description')
    result = fields.Text(string='classification result')

    def load_ticketing_model(self):
        """
        Load the pre-trained FastText model from the data directory.
        """
        model_path = os.path.join("C:/Users/Yasmine/odoo/Custom_modules/ticketing/data", 'fasttext_ticket_classifier_augmented.bin')
        print(model_path)
        try:
            model = load_model(model_path)
            return model
        except Exception as e:
            print(f"Error loading the model: {str(e)}")
            return None

    def classify_ticket(self, description):
        """
        Classifies a ticket description using a pre-trained FastText model.
        """
        # Ensure description is a string and sanitize it
        if description is None:
            raise ValueError("Description cannot be None.")
        description = str(description).strip().replace("\n", " ")  # Remove newlines
        print(f"Sanitized description: {description}")  # Debugging info

        model = self.load_ticketing_model()

        if model is not None:
            try:
                prediction = model.predict(description, k=1)  # k=1 for top prediction
                print(f"Prediction result: {prediction}")  # Debugging info
                predicted_class = prediction[0][0]  # Extract the predicted label
                return predicted_class
            except Exception as e:
                print(f"Error during prediction: {str(e)}")
                return None
        else:
            return None


    def action_classify_ticket(self):
        print("Classify Ticket button clicked!")  # Debug: Check if action is triggered
        for ticket in self:
            print(f'ticket: {ticket}')
            description = ticket.ticket_description
            classification_result = ticket.classify_ticket(description)
            self.result = classification_result
            print(f"Classification result: {classification_result}")  # Debug: Check result

