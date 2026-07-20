from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# PASTE YOUR TMDB API KEY HERE:
TMDB_API_KEY = "861edbc9c659c8714873ca4ae6edee8c"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

@app.route('/')
def home():
    # Get popular movies
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    movies = response.json().get('results', [])[:12]
    return render_template('index.html', movies=movies)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
        response = requests.get(url)
        movies = response.json().get('results', [])
        return render_template('index.html', movies=movies, query=query)
    return render_template('index.html', movies=[])

@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    # Get movie details
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    movie = requests.get(url).json()
    
    # Video source (VidSrc)
    video_url = f"https://vidsrc.cc/v2/embed/movie/{movie_id}"
    
    return render_template('detail.html', movie=movie, video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)