from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ============================================
# CONFIGURATION
# ============================================
TMDB_API_KEY = "861edbc9c659c8714873ca4ae6edee8c"  # <--- PASTE YOUR TMDB API KEY HERE
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# List of video sources (will try in order)
VIDEO_SOURCES = [
    "https://multiembed.mov/?video_id={movie_id}",
    "https://www.2embed.cc/embed/{movie_id}",
    "https://vidsrc.to/embed/movie/{movie_id}",
    "https://vidsrc.xyz/embed/movie/{movie_id}",
    "https://vidsrc.pro/embed/movie/{movie_id}",
    "https://vidembed.cc/embed/movie/{movie_id}",
    "https://embed.su/embed/movie/{movie_id}",
    "https://movie-web.app/embed/movie/{movie_id}",
]


# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    """Homepage - Show popular movies"""
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    movies = response.json().get('results', [])[:20]
    return render_template('index.html', movies=movies)


@app.route('/search')
def search():
    """Search for movies"""
    query = request.args.get('q', '')
    movies = []
    if query:
        url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
        response = requests.get(url)
        movies = response.json().get('results', [])
    return render_template('index.html', movies=movies, query=query)


@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    """Movie details page with video player"""
    # Get movie details from TMDB
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    movie = response.json()
    
    # Generate all video source URLs
    video_urls = []
    for source_template in VIDEO_SOURCES:
        video_urls.append(source_template.format(movie_id=movie_id))
    
    return render_template(
        'detail.html', 
        movie=movie, 
        video_urls=video_urls,
        primary_video_url=video_urls[0]  # First one is primary
    )


# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)