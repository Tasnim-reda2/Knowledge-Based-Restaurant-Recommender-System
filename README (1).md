
# Knowledge-Based Restaurant Recommender System

## 📝 Project Overview
This project is a **Knowledge-Based Restaurant Recommender System** developed using the Zomato dataset. Unlike collaborative filtering models, this system is built on explicit user preferences such as:

- Cuisine type
- Price range
- Country/location

The system uses rule-based filtering and a scoring method based on restaurant ratings and vote counts to suggest top recommendations.

---

## 🗃️ Dataset Used
- **Zomato.csv** – Restaurant data (name, location, cuisines, ratings, etc.)
- **Country-Code.xlsx** – Mapping of country codes to country names

---

## ⚙️ Modules and Features

### ✅ Data Processing Scripts
- Load and clean data using pandas
- Normalize cuisine names
- Categorize price levels into Low, Medium, High
- Extract primary cuisine from multi-cuisine fields

### ✅ User Preference Interface
- Developed with **Streamlit**
- Sidebar for selecting:
  - Cuisines
  - Price range
  - Country
  - Number of recommendations

### ✅ Recommendation Engine
- `filter_and_rank()` function
  - Filters restaurants by user preferences
  - Scores based on weighted average: 70% rating + 30% number of votes
  - Returns top-N matching restaurants

### ✅ User Interface
- Streamlit-based web interface
- Shows restaurant details and a short explanation for each recommendation

---

## 🧪 Evaluation Summary
- **User Feedback:** Average rating 4.6/5 for relevance, 4.8/5 for ease of use
- **A/B Testing:** Strategy with weighted rating favored by users

---

## 🚀 Deployment
- Can be hosted on **Streamlit Cloud** or **Render**
- Upload code to GitHub and deploy with minimal setup

---

## 📌 Future Improvements
- Add map view for visualizing restaurant locations
- Enhance filtering (e.g., by city or delivery availability)
- Add NLP-based search (e.g., “cheap Chinese in Delhi”)
- Improve mobile UI responsiveness

---

## 👨‍💻 Author
Developed as part of a knowledge-based AI application project using Python and Streamlit.
