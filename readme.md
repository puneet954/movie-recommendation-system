# movie-recommendation-system
# 🎬 Movie Recommendation System

A Machine Learning based Movie Recommendation System that suggests movies to users based on content similarity. The system analyzes movie features such as genres, keywords, cast, crew, and overview to recommend movies similar to the selected one.

---

# 📌 Project Overview

This project uses **Content-Based Filtering** to recommend movies.  
It compares movies using textual metadata and finds similarity between them using **Cosine Similarity**.

When a user selects a movie, the system recommends movies with similar content and characteristics.

---

# 🚀 Features

- Movie recommendation based on similarity
- Content-based filtering approach
- Fast similarity search using cosine similarity
- Clean and interactive interface
- Search functionality
- Dataset preprocessing and feature engineering
- Model serialization using Pickle

---

# 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Streamlit
- Pickle

---

# 📂 Dataset

The project uses the TMDB Movie Dataset containing:

- Movie title
- Genres
- Keywords
- Cast
- Crew
- Overview

---

# ⚙️ Working Process

1. Data Collection
2. Data Cleaning
3. Feature Extraction
4. Text Vectorization using CountVectorizer
5. Similarity Calculation using Cosine Similarity
6. Recommendation Generation

---

# 🧠 Machine Learning Concepts Used

- Natural Language Processing (NLP)
- Text Vectorization
- Cosine Similarity
- Content-Based Recommendation System

---

# 📸 Output

The system recommends top similar movies based on the selected movie.

Example:

```python
Input Movie: Avatar

Recommended Movies:
- Guardians of the Galaxy
- John Carter
- Star Trek
- The Avengers
- Alien