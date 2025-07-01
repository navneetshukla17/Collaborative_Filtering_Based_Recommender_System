import os
import sys
import pickle
import streamlit as st
import numpy as np
import time
from datetime import datetime
from sklearn.metrics.pairwise import cosine_distances
from Collaborative_Filtering_Based_Recommender_System.logger.log import logging
from Collaborative_Filtering_Based_Recommender_System.config.configuration import AppConfiguration
from Collaborative_Filtering_Based_Recommender_System.pipeline.training_pipeline import TrainingPipeline
from Collaborative_Filtering_Based_Recommender_System.exception.exception_handler import AppException

st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="wide")

BASE_DIR = os.getcwd()

def load_pickle_file(relative_path):
    absolute_path = os.path.join(BASE_DIR, relative_path)
    try:
        with open(absolute_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading {relative_path}")
        raise AppException(e, sys) from e

def check_file_exists(filepath):
    return os.path.exists(filepath)

class Recommendation:
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def fetch_poster(self, suggestion):
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot = load_pickle_file(self.recommendation_config.book_pivot_serialized_objects)
            final_rating = load_pickle_file(self.recommendation_config.final_rating_serialized_objects)

            placeholder_image = "https://via.placeholder.com/150?text=No+Image"

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]:
                ids = np.where(final_rating['title'] == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = final_rating.iloc[idx]['image_url']
                if not url or url.strip() == "" or url.lower() == "nan":
                    poster_url.append(placeholder_image)
                else:
                    poster_url.append(url)

            return poster_url
        except Exception as e:
            raise AppException(e, sys) from e

    def recommend_book(self, book_name):
        try:
            books_list = []
            book_pivot = load_pickle_file(self.recommendation_config.book_pivot_serialized_objects)
            book_id = np.where(book_pivot.index == book_name)[0][0]

            distances = cosine_distances(book_pivot.iloc[book_id, :].values.reshape(1, -1), book_pivot)[0]
            recommended_indices = np.argsort(distances)[1:]

            for idx in recommended_indices:
                books_list.append(book_pivot.index[idx])

            poster_url = self.fetch_poster([recommended_indices])

            return books_list, poster_url
        except Exception as e:
            raise AppException(e, sys) from e

    def train_engine(self):
        try:
            obj = TrainingPipeline()
            progress_text = "⏳ Training model, please wait..."
            progress_bar = st.progress(0, text=progress_text)

            for percent_complete in range(0, 100, 10):
                time.sleep(0.5)  # Simulated step
                progress_bar.progress(percent_complete + 10, text=f"Training Progress: {percent_complete + 10}%")

            with st.spinner('Finalizing training...'):
                obj.start_training_pipeline()

            with open('last_trained.txt', 'w') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            st.success("✅ Training Completed Successfully!")
            logging.info(f"Recommended successfully!")

            st.session_state.model_trained = True
            st.session_state.notification = "✅ Model Trained Successfully! You can now get recommendations."

            st.rerun()

        except Exception as e:
            st.error("⚠️ Training failed. Please check logs.")
            raise AppException(e, sys) from e

# ------------------- Streamlit UI -------------------

if __name__ == "__main__":
    st.markdown(
        """
        <style>
            .main { display: flex; flex-direction: column; align-items: center; justify-content: center; }
            .stButton > button { width: 250px; margin: 10px 0; background-color: white; color: black; border: 1px solid #999; border-radius: 10px; font-weight: bold; font-size: 16px; }
            .stSelectbox label { font-size: 18px; }
            .stSelectbox div[data-baseweb="select"] { width: 100% !important; }
            .pagination-container { display: flex; justify-content: center; align-items: center; gap: 40px; margin-top: 20px; }
            .hover-effect { transition: transform 0.3s ease; cursor: pointer; }
            .hover-effect:hover { transform: scale(1.1); }
            img { border-radius: 0 !important; }
            body { font-family: 'Georgia', serif; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('Collaborative Book Recommender System 📚')
    st.markdown("This is a **Collaborative Filtering Based Recommendation System**. Get book suggestions based on your selection!")

    obj = Recommendation()

    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = check_file_exists(os.path.join('artifacts', 'serialized_objects', 'book_pivot.pkl'))

    if 'recommended_books' not in st.session_state:
        st.session_state.recommended_books = []
    if 'poster_urls' not in st.session_state:
        st.session_state.poster_urls = []
    if 'page' not in st.session_state:
        st.session_state.page = 0

    if 'notification' in st.session_state:
        st.success(st.session_state.notification)
        del st.session_state.notification

    if not st.session_state.model_trained:
        st.warning("⚠️ Model not trained yet. Please first train the model to get recommendations. Click the button below to train the model.")

    st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
    if st.button('Train Recommender System'):
        obj.train_engine()
    st.markdown("</div>", unsafe_allow_html=True)

    book_names = load_pickle_file(os.path.join('templates', 'book_names.pkl'))

    st.markdown("---")
    st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
    selected_books = st.selectbox("🔍 Select a Book to Get Recommendations:", book_names)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
    show_button = st.button('Show Recommendations', disabled=not st.session_state.model_trained)
    if show_button:
        if st.session_state.model_trained:
            with st.spinner('🔎 Fetching best book matches for you...'):
                books, posters = obj.recommend_book(selected_books)
                st.session_state.recommended_books = books
                st.session_state.poster_urls = posters
                st.session_state.page = 0
        else:
            st.warning("⚠️ Please train the model first before getting recommendations.")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.recommended_books:
        st.markdown("---")
        st.subheader(f"📚 Recommended Books for: **{selected_books}**")

        per_page = 15
        total_pages = (len(st.session_state.recommended_books) + per_page - 1) // per_page
        start = st.session_state.page * per_page
        end = start + per_page

        current_books = st.session_state.recommended_books[start:end]
        current_posters = st.session_state.poster_urls[start:end]

        with st.expander("📖 View Recommendations", expanded=True):
            cols = st.columns(5)

            for i, (bk, pt) in enumerate(zip(current_books, current_posters)):
                with cols[i % 5]:
                    st.markdown(
                        f"""
                        <a href="{pt}" target="_blank">
                            <img src="{pt}" class="hover-effect" width="300" />
                        </a>
                        <div style='text-align: center; font-weight: bold;'>{bk}</div>
                        """,
                        unsafe_allow_html=True
                    )

                if (i + 1) % 5 == 0 and (i + 1) != len(current_books):
                    cols = st.columns(5)

        st.markdown('<div class="pagination-container">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 0.5, 1])

        with col1:
            st.markdown("<div style='display: flex; justify-content: flex-end;'>", unsafe_allow_html=True)
            if st.session_state.page > 0:
                if st.button("⇤ Previous"):
                    st.session_state.page -= 1
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown(f"**Page {st.session_state.page + 1} / {total_pages}**", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            if st.session_state.page < total_pages - 1:
                if st.button("Next ⇥"):
                    st.session_state.page += 1
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

#------------Final version with all the features and improvements------------#


