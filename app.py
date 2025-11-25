import streamlit as st
import os 
import json
from helper_func import *
import datetime

st.title("RateMyDate")

# ---------------------------
# SESSION STATE SETUP
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = 1
if "date_name" not in st.session_state:
    st.session_state.date_name = ""

# ---------------------------
# Questions and Ratings
# ---------------------------
questions = [
        f"How well were {st.session_state.date_name}'s conversational skills?",
        f"How was {st.session_state.date_name}'s punctuality? (early, on-time, late)",
        f"How was {st.session_state.date_name}'s hygiene? (clean, scent)",
        f"How well did {st.session_state.date_name} respect you, the staff, and your time?",
        f"How was your chemistry with {st.session_state.date_name}?",
        f"BONUS: How well do you feel seen and heard around {st.session_state.date_name}?"
    ]

ratings = ["NA: Enter a Response","-2: Well Below Expectations","-1: Below Expectations", "0: Neutral", "+1: Met Expectations", "+2: Exceeded Expectations"]

# ---------------------------
# SESSION STATE SETUP
# ---------------------------
if "answers" not in st.session_state or st.button("New Entry"):
    st.session_state.answers = [0] * len(questions)

# ---------------------------
# PAGE 1 — GET Date Name
# ---------------------------
if st.session_state.page == 1:
    date_name = st.text_input("Who did you go on a date with?", placeholder="Enter Name")

    if st.button("Next") and date_name:
        st.session_state.date_name = date_name
        st.session_state.page = 2

# ---------------------------
# PAGE 2 — QUESTIONS WITH DROPDOWNS
# ---------------------------
elif st.session_state.page == 2:
    # Show all questions at once
    labels = {
        -2: "Horrible",
        -1: "Poor",
         0: "Average",
         1: "Above Average",
         2: "Great"
    }

    # Convert label dict into a list of label strings
    rating_options = list(labels.values())

    for i, q in enumerate(questions):
#        st.write(q)
        selected_label = st.selectbox(
            q,
            rating_options,
            index=2, 
            key=f"q{i}"
        )
        # Convert selected label back to numeric value
        numeric_value = [k for k, v in labels.items() if v == selected_label][0]
        st.session_state.answers[i] = numeric_value

    if st.button("Done"):
        st.session_state.page = 3

# ---------------------------
# PAGE 3 — SCORE & SUMMARY
# ---------------------------        
elif st.session_state.page == 3:
    st.write("Your answers:")
    total_score = sum(a for a in st.session_state.answers if isinstance(a, int))

    # If all questions answered, show total & recommendation
    st.write(f"**Total Score:** {total_score}")
    recommendation = get_recommendation(total_score)
    st.write(f"Recommendation: {recommendation}")

    # Button to start a new entry
    if st.button("New Entry"):
        st.session_state.page = 1
        st.session_state.answers = [0] * len(questions)   
        st.session_state.date_name = ""
        st.session_state.date_age = ""
        st.session_state.date_date = ""

    
