import requests
import re
import os
import json
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
APP_FILE = "app.py"  # Your main app file
SOURCES_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/sources.txt"  # Your own source list
# OR use a public source list (see below)

# ============================================
# FUNCTION TO FETCH SOURCES
# ============================================

def fetch_sources():
    """
    Fetch video sources from a remote URL.
    Returns a list of source URLs.
    """
    try:
        # Option 1: Fetch from a GitHub raw URL (you maintain this list)
        response = requests.get(SOURCES_URL, timeout=10)
        if response.status_code == 200:
            sources = response.text.strip().split('\n')
            # Clean up and filter empty lines
            sources = [s.strip() for s in sources if s.strip() and not s.startswith('#')]
            if sources:
                print(f"✅ Fetched {len(sources)} sources from remote")
                return sources
        
        # Option 2: If remote fails, use local fallback
        print("⚠️ Remote fetch failed, using local fallback...")
        return get_local_fallback()
        
    except Exception as e:
        print(f"❌ Error fetching sources: {e}")
        return get_local_fallback()

def get_local_fallback():
    """
    Local fallback sources (if remote fetch fails)
    """
    return [
        "https://autoembed.co/embed/movie/{movie_id}",
        "https://vidsrc.pm/embed/movie/{movie_id}",
        "https://2embed.skin/embed/movie/{movie_id}",
        "https://vidsrc.mov/embed/movie/{movie_id}",
        "https://multiembed.mov/?video_id={movie_id}",
        "https://vidfast.co/embed/movie/{movie_id}",
    ]

# ============================================
# FUNCTION TO UPDATE APP.PY
# ============================================

def update_app_file(sources):
    """
    Update the VIDEO_SOURCES list in app.py
    """
    try:
        # Read the current app.py
        with open(APP_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the VIDEO_SOURCES list and replace it
        # Pattern to find VIDEO_SOURCES = [...]
        pattern = r'(VIDEO_SOURCES\s*=\s*\[)(.*?)(\])'
        
        # Build the new list as a string
        sources_str = ',\n    '.join([f'"{s}"' for s in sources])
        new_list = f'VIDEO_SOURCES = [\n    {sources_str}\n]'
        
        # Replace in content
        new_content = re.sub(pattern, new_list, content, flags=re.DOTALL)
        
        # Write the updated content
        with open(APP_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated {APP_FILE} with {len(sources)} sources")
        return True
        
    except Exception as e:
        print(f"❌ Error updating app.py: {e}")
        return False

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    print(f"🔄 Updating video sources... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Fetch sources
    sources = fetch_sources()
    
    if sources:
        # Update app.py
        success = update_app_file(sources)
        
        if success:
            print("✅ Sources updated successfully!")
        else:
            print("❌ Failed to update sources.")
    else:
        print("❌ No sources found to update.")

if __name__ == "__main__":
    main()