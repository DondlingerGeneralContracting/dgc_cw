# LLAMA Chat Interface with TOR

Interactive web interface for chatting with LLAMA AI models using the LLAMA API, routed through TOR for anonymity.

## Local Setup with TOR

1. Install Python dependencies: `pip install -r requirements.txt`
2. Download and extract TOR expert bundle (included in `tor/` folder)
3. Start TOR: `cd tor; .\tor.exe` (runs in background)
4. Replace 'YOUR_API_KEY' in `app.py` with your actual LLAMA API key
5. Run the app: `python app.py`
6. Open http://localhost:5000 in your browser

The API calls to LLAMA are proxied through TOR for enhanced privacy.

## GitHub Pages (Static Version)

A static version is available on GitHub Pages at https://dondlingergeneralcontracting.github.io/dgc_cw/, but without TOR routing.

### Website Structure

- `index.html` - Main website page with chat interface
- `styles.css` - Styling and responsive design
- `.github/workflows/pages.yml` - GitHub Pages deployment workflow

## Features

- Interactive chat with LLAMA models via API
- Powered by LLAMA API client
- Responsive design for mobile, tablet, and desktop
- Real-time chat interface
- Seamless API integration
