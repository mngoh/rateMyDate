# Helper functions for RateMyDate

def get_recommendation(score):
    date_outcomes = {
            (-12,0): "This was a Horrible date: RUN",
            (0,4): "This was a poor date, reach out as soon as possible to express your feelings and move on.",
            (4, 8): "This was an Above Average Date: Consider a second date after reflecting.",
            (8, 12): "This was a GREAT DATE: Decide in the next day how you'd like to proceed."
        }
    for (lower, upper), message in date_outcomes.items():
        if lower < score <= upper:  
            return message
    return "Score out of range"