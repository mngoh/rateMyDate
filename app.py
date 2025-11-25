import streamlit as st
import os 
import json
from helper_func import *
import datetime

st.title("RateMyDate")
# Test
# ---------------------------
# SESSION STATE SETUP
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = 1
if "date_name" not in st.session_state:
    st.session_state.date_name = ""
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ---------------------------
# Questions and Ratings
# ---------------------------
questions = [
        f"How well were {st.session_state.date_name}'s conversational skills?",
        f"How was {st.session_state.date_name}'s punctuality? (early, on-time, late)",
        f"How was {st.session_state.date_name}'s hygiene? (clean, scent)",
        f"Did {st.session_state.date_name} respect you, the staff, and your time?",
        f"Did you and {st.session_state.date_name} have good chemistry?",
        f"BONUS: How well do you feel seen and heard around {st.session_state.date_name}?"
    ]

ratings = ["NA: Enter a Response","-2: Well Below Expectations","-1: Below Expectations", "0: Neutral", "+1: Met Expectations", "+2: Exceeded Expectations"]

# ---------------------------
# PAGE 1 — GET DATE NAME, date of date, and age of date
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
        -1: "Bad",
        0: "Average",
        1: "Above Average",
        2: "Great"
    }

    for i, q in enumerate(questions):
        st.write(q)
        answer = st.slider(
            "",  # keep the question above instead
            min_value=-2,
            max_value=2,
            value=0,
            step=1,
            key=f"q{i}"
        )
        st.write("Selected:", labels[answer])
        st.session_state.answers[i] = answer

    if st.button("Done"):
        st.session_state.page = 3

# ---------------------------
# PAGE 3 — SCORE & SUMMARY
# ---------------------------        
elif st.session_state.page == 3:
    st.write("Your answers:")

    total_score = 0
    all_answered = True

    # If all questions answered, show total & recommendation
    if all_answered:
        st.write(f"**Total Score:** {total_score}")
        recommendation = get_recommendation(total_score)
        st.write(f"Recommendation: {recommendation}")
    else:
        st.error("ERROR: Please enter a score for all questions before viewing the total.")

    # Button to start a new entry
    if st.button("New Entry"):
        st.session_state.page = 1
        st.session_state.answers = ["NA"] * len(questions)
        st.session_state.date_name = ""
        st.session_state.date_age = ""
        st.session_state.date_date = ""

    
