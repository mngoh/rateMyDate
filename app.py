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
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ---------------------------
# Questions and Ratings
# ---------------------------
questions = [
        f"How well were {st.session_state.date_name}'s conversational skills?",
        f"How was {st.session_state.date_name}'s punctuality? (early, on-time, late)",
        f"How was {st.session_state.date_name}'s hygiene? (clean teeth, scent)",
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
    date_date = st.date_input("Date of Date:")
    date_age = st.number_input("Date's Age:", step=1, min_value=20, max_value=40, placeholder=25)

    if st.button("Next") and date_name and date_age and date_date:
        st.session_state.date_name = date_name
        st.session_state.date_age = date_age
        st.session_state.date_date = date_date

        st.session_state.page = 2

# ---------------------------
# PAGE 2 — QUESTIONS WITH DROPDOWNS
# ---------------------------
elif st.session_state.page == 2:
    # Show all questions at once
    for i, q in enumerate(questions):
        st.session_state.answers[i] = st.selectbox(q, ratings, key=f"q{i}")

    if st.button("Done"):
        st.session_state.page = 3

# ---------------------------
# PAGE 3 — SCORE & SUMMARY
# ---------------------------
elif st.session_state.page == 3:
    st.write(f"### Thanks for rating {st.session_state.date_name}!")
    st.write("Your answers:")

    total_score = 0
    all_answered = True

    # Build Markdown string for nested bullets
    md_output = ""
    for i, q in enumerate(questions):
        ans = st.session_state.answers[i]
        if ans == "NA":
            all_answered = False
        else:
            try:
                score = int(ans.split(":")[0])
                total_score += score
            except (ValueError, IndexError):
                all_answered = False

        # Nested bullet formatting
        md_output += f"- **{q}**\n  - {ans}\n"

    st.markdown(md_output)

    # If all questions answered, show total & recommendation
    if all_answered:
        st.write(f"**Total Score:** {total_score}")
        recommendation = get_recommendation(total_score)
        st.write(f"Recommendation: {recommendation}")

        # Build result dict
        result = {
            "date_name": st.session_state.date_name,
            "date_age": st.session_state.date_age,
            # Convert date object to string (YYYY-MM-DD)
            "date_date": st.session_state.date_date.isoformat() if isinstance(st.session_state.date_date, (datetime.date, datetime.datetime)) else st.session_state.date_date,
            "total_score": total_score,
            "questions": questions,
            "answers": st.session_state.answers
        }

        # Save result to JSON
        file_path = "results.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Avoid duplicates
        exists = any(
            entry.get("date_name") == result["date_name"] and
            entry.get("date_age") == result["date_age"] and
            entry.get("date_date") == result["date_date"]
            for entry in data
        )

        if not exists:
            data.append(result)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Your results have been saved!")
        else:
            st.info("This entry already exists. No new data was saved.")
    else:
        st.error("ERROR: Please enter a score for all questions before viewing the total.")

    # Button to start a new entry
    if st.button("New Entry"):
        st.session_state.page = 1
        st.session_state.answers = ["NA"] * len(questions)
        st.session_state.date_name = ""
        st.session_state.date_age = ""
        st.session_state.date_date = ""

    
