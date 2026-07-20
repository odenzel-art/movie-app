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
    # ============================================
    # TIER 1: Most Reliable (Tested Working)
    # ============================================
    "https://autoembed.co/embed/movie/{movie_id}",
    "https://vidsrc.pm/embed/movie/{movie_id}",
    "https://2embed.skin/embed/movie/{movie_id}",
    "https://vidsrc.mov/embed/movie/{movie_id}",
    "https://multiembed.mov/?video_id={movie_id}",
    "https://vidfast.co/embed/movie/{movie_id}",
    
    # ============================================
    # TIER 2: Recently Working
    # ============================================
    "https://moviesapi.to/embed/movie/{movie_id}",
    "https://frembed.xyz/embed/movie/{movie_id}",
    "https://embed.su/embed/movie/{movie_id}",
    "https://vidsrc.xyz/embed/movie/{movie_id}",
    "https://vidsrc.to/embed/movie/{movie_id}",
    "https://vidembed.cc/embed/movie/{movie_id}",
    
    # ============================================
    # TIER 3: Alternative Domains
    # ============================================
    "https://2embed.cc/embed/movie/{movie_id}",
    "https://2embed.org/embed/movie/{movie_id}",
    "https://2embed.li/embed/movie/{movie_id}",
    "https://vidsrc.net/embed/movie/{movie_id}",
    "https://vidsrc.pro/embed/movie/{movie_id}",
    "https://vidsrc.info/embed/movie/{movie_id}",
    "https://moviesapi.net/embed/movie/{movie_id}",
    
    # ============================================
    # TIER 4: Extra Sources
    # ============================================
    "https://vidcloud.cc/embed/movie/{movie_id}",
    "https://vidstream.cc/embed/movie/{movie_id}",
    "https://vidplay.cc/embed/movie/{movie_id}",
    "https://movie-web.app/embed/movie/{movie_id}",
    "https://watch.qtvideo.xyz/embed/movie/{movie_id}",
    "https://play.flixhq.to/embed/movie/{movie_id}",
    "https://v3.vidsrc.cc/embed/movie/{movie_id}",
    "https://v4.vidsrc.cc/embed/movie/{movie_id}",
]


# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    # Get popular movies from TMDB
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    movies = response.json().get('results', [])[:20]
    
    # Watch history (frontend will handle it via localStorage)
    watch_history = {}
    
    return render_template('index.html', movies=movies, watch_history=watch_history)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    movies = []
    if query:
        url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
        response = requests.get(url)
        movies = response.json().get('results', [])
    
    # Add watch_history here too
    watch_history = {}
    
    return render_template('index.html', movies=movies, query=query, watch_history=watch_history)


@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    # Get movie details from TMDB
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    movie = response.json()
    
    # Generate all video source URLs
    video_urls = []
    for source_template in VIDEO_SOURCES:
        video_urls.append(source_template.format(movie_id=movie_id))
    
    # Pass all sources to the template
    return render_template(
        'detail.html', 
        movie=movie, 
        video_urls=video_urls,
        primary_video_url=video_urls[0]
    )


# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)