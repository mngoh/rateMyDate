# Helper functions for RateMyDate

def get_recommendation(score):
    date_outcomes = {
            (-20, 0): "This was a POOR date: Reach out, express your feelings, and MOVE ON.",
            (0, 5): "This was an Average Date: Assess your feelings over the next couple of days and come to a conclusion.",
            (5, 10): "This was an Above Average Date: Consider a second date if you feel good.",
            (10, 12): "This was a GREAT DATE: Decide in the next day how you'd like to set up the second date."
        }
    for (lower, upper), message in date_outcomes.items():
        if lower < score <= upper:  
            return message
    return "Score out of range"