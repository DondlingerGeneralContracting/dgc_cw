# LLAMA Chat Interface

Interactive web interface for chatting with LLAMA AI models using the LLAMA API client.

## GitHub Pages

This website is deployed using GitHub Pages. The site is automatically deployed when changes are pushed to the `main` branch.

### Local Development

To run the application locally:

1. Install dependencies: `pip install -r requirements.txt`
2. Set your LLAMA API key: `export LLAMA_API_KEY=your-key-here`
3. Run the server: `python app.py`
4. Open http://localhost:5000 in your browser

### Website Structure

- `index.html` - Main website page with chat interface
- `styles.css` - Styling and responsive design
- `app.py` - Flask backend server with LLAMA API integration
- `requirements.txt` - Python dependencies
- `.github/workflows/pages.yml` - GitHub Pages deployment workflow

## Features

- Interactive chat with LLAMA models via API
- Powered by LLAMA API client
- Responsive design for mobile, tablet, and desktop
- Real-time chat interface
- Seamless API integration
