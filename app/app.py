import streamlit as st
import pickle
import pandas as pd
import requests
from urllib.parse import quote

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch · Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# ── TMDB Config ───────────────────────────────────────────────────────────────
TMDB_API_KEY = "9778b8036b77015f291f84d1a44cccef"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
FALLBACK_POSTER = "https://via.placeholder.com/300x450/14141f/c9a84c?text=No+Poster"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e4dc;
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #1a0a2e 0%, #0a0a0f 55%),
                radial-gradient(ellipse at 80% 100%, #0d1a2e 0%, transparent 60%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 1px; height: 50px;
    background: linear-gradient(to bottom, transparent, #c9a84c);
}
.hero-tag {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c9a84c;
    margin: 1rem 0 0.8rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 7vw, 4.5rem);
    font-weight: 900;
    line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 30%, #c9a84c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero-sub {
    font-size: 0.95rem;
    color: #8a8070;
    margin-top: 0.8rem;
    font-weight: 300;
}

.gold-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #c9a84c55, transparent);
    margin: 2rem 0;
}

/* ── Select label ── */
.select-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 0.5rem;
    text-align: center;
}

/* ── Streamlit selectbox override ── */
div[data-baseweb="select"] > div {
    background-color: #12121a !important;
    border: 1px solid #2a2535 !important;
    border-radius: 8px !important;
    color: #e8e4dc !important;
}
div[data-baseweb="select"] > div:hover { border-color: #c9a84c !important; }
div[data-baseweb="select"] svg { fill: #c9a84c !important; }

/* ── Button ── */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #c9a84c, #a07830);
    color: #0a0a0f;
    border: none;
    border-radius: 8px;
    padding: 0.85rem 2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    cursor: pointer;
    margin-top: 0.8rem;
    transition: opacity 0.2s, transform 0.15s;
}
div.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }
div.stButton > button:active { transform: translateY(0); }

/* ── Section title ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin: 2rem 0 1.5rem;
    text-align: center;
}
.section-title em { color: #c9a84c; font-style: italic; }

/* ── Poster card ── */
.poster-card-link {
    text-decoration: none;
    display: block;
}

.poster-card {
    background: linear-gradient(160deg, #14141f, #1a1625);
    border: 1px solid #22203080;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
    animation: fadeUp 0.5s ease both;
    cursor: pointer;
    position: relative;
}
.poster-card:hover {
    transform: translateY(-8px);
    border-color: #c9a84c99;
    box-shadow: 0 24px 48px #0009, 0 0 0 1px #c9a84c33;
}

/* ── Play overlay on hover ── */
.poster-card .overlay {
    position: absolute;
    top: 0; left: 0; right: 0;
    aspect-ratio: 2/3;
    background: linear-gradient(160deg, #0008, #c9a84c22);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.25s;
}
.poster-card:hover .overlay { opacity: 1; }

.play-btn {
    width: 54px; height: 54px;
    border-radius: 50%;
    background: #c9a84c;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 20px #0006;
    font-size: 1.3rem;
    color: #0a0a0f;
    font-weight: 900;
    padding-left: 4px;  /* optical center for play triangle */
}

.watch-badge {
    position: absolute;
    top: 10px; right: 10px;
    background: #c9a84c;
    color: #0a0a0f;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.22rem 0.55rem;
    border-radius: 20px;
    opacity: 0;
    transition: opacity 0.25s;
}
.poster-card:hover .watch-badge { opacity: 1; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.poster-card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    border-bottom: 1px solid #22203080;
}

.poster-info {
    padding: 0.85rem 0.9rem 1rem;
}
.poster-rank {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #c9a84c;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.poster-title {
    font-size: 0.9rem;
    font-weight: 500;
    color: #e8e4dc;
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.watch-hint {
    font-size: 0.68rem;
    color: #c9a84c88;
    margin-top: 0.45rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

/* ── Tooltip ── */
.tooltip-text {
    font-size: 0.72rem;
    color: #6a6070;
    text-align: center;
    margin-top: 1.2rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 4rem;
    font-size: 0.7rem;
    color: #3a3540;
    letter-spacing: 0.12em;
}
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
import os
import gdown


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, '..', 'artifacts')

@st.cache_resource
def load_data():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    movie_dict_path = os.path.join(ARTIFACTS_DIR, 'movie_dict.pkl')
    similarity_path = os.path.join(ARTIFACTS_DIR, 'similarity.pkl')
    
    if not os.path.exists(movie_dict_path):
        gdown.download(
            'https://drive.google.com/uc?id=1luM9VcjOA7YyoANGd60ed0fi95P31VN3',
            movie_dict_path,
            quiet=False
        )
    
    if not os.path.exists(similarity_path):
        gdown.download(
            'https://drive.google.com/uc?id=1-YnbtpA0lQP4BpaZNBVaBaTRHOmCeeTf',
            similarity_path,
            quiet=False
        )
        
    
    movies_dict = pickle.load(open(movie_dict_path, 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open(similarity_path, 'rb'))
    return movies, similarity

movies, similarity = load_data()


# ── TMDB: fetch poster + IMDB id ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_movie_data(movie_title):
    """Returns (poster_url, watch_url) for a given title."""
    try:
        # 1. Search for the movie
        search_resp = requests.get(
            f"{TMDB_BASE_URL}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": movie_title},
            timeout=5,
        ).json()

        results = search_resp.get("results", [])
        if not results:
            return FALLBACK_POSTER, f"https://www.google.com/search?q={quote(movie_title + ' watch online free')}"

        top = results[0]
        movie_id = top.get("id")

        # 2. Poster
        poster_path = top.get("poster_path")
        poster_url = (POSTER_BASE_URL + poster_path) if poster_path else FALLBACK_POSTER

        # 3. Get external IDs (IMDB id)
        ext_resp = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}/external_ids",
            params={"api_key": TMDB_API_KEY},
            timeout=5,
        ).json()
        imdb_id = ext_resp.get("imdb_id")

        # 4. Build watch URL
        if imdb_id:
            # Links to IMDb page – users can find streaming options from there
            watch_url = f"https://www.imdb.com/title/{imdb_id}/"
        else:
            watch_url = f"https://www.google.com/search?q={quote(movie_title + ' watch online free')}"

        return poster_url, watch_url

    except Exception:
        return FALLBACK_POSTER, f"https://www.google.com/search?q={quote(movie_title + ' watch online free')}"


# ── Recommendation logic ───────────────────────────────────────────────────────
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movies_list]


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ AI-Powered Discovery ✦</div>
    <h1 class="hero-title">CineMatch</h1>
    <p class="hero-sub">Tell us what you love — we'll find your next obsession.</p>
</div>
<div class="gold-divider"></div>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    st.markdown('<div class="select-label">🎬 &nbsp; Choose a Movie</div>', unsafe_allow_html=True)
    selected_movie_name = st.selectbox(
        label="",
        options=movies['title'].values,
        label_visibility="collapsed",
    )
    recommend_clicked = st.button("✦  Discover Similar Films  ✦")

# ── Results ────────────────────────────────────────────────────────────────────
if recommend_clicked:
    with st.spinner("Fetching recommendations & posters..."):
        recommendations = recommend(selected_movie_name)
        movie_data = [fetch_movie_data(title) for title in recommendations]

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-title">Because you liked <em>{selected_movie_name}</em>…</div>',
        unsafe_allow_html=True
    )

    ranks = ["01", "02", "03", "04", "05"]
    cols = st.columns(5)

    for col, title, (poster, watch_url), rank in zip(cols, recommendations, movie_data, ranks):
        with col:
            st.markdown(f"""
            <a href="{watch_url}" target="_blank" class="poster-card-link">
                <div class="poster-card">
                    <div class="overlay">
                        <div class="play-btn">▶</div>
                    </div>
                    <span class="watch-badge">▶ Watch</span>
                    <img src="{poster}" alt="{title}"
                         onerror="this.src='{FALLBACK_POSTER}'"/>
                    <div class="poster-info">
                        <div class="poster-rank">Pick {rank}</div>
                        <div class="poster-title">{title}</div>
                        <div class="watch-hint">🎬 Click to watch</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    st.markdown(
        '<div class="tooltip-text">🔗 Clicking a poster opens its IMDb page where you can find streaming options.</div>',
        unsafe_allow_html=True
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">CINEMATCH &nbsp;·&nbsp; POWERED BY TMDB & IMDB &nbsp;·&nbsp; 2025</div>',
    unsafe_allow_html=True
)


