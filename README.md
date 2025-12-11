# LLAMA Chat Interface with TOR Hidden Service

Interactive web interface for chatting with LLAMA AI models, with API hosted on TOR hidden service for maximum privacy.

## Docker Setup for TOR Hidden Service API

1. Set environment variables:
   ```
   export LLAMA_API_KEY="your_llama_api_key_here"
   export LLAMA_API_URL="https://api.llama.com/v1/chat/completions"
   ```

2. Build and run the Docker container:
   ```
   cd docker
   docker-compose up --build
   ```

3. The container will output your .onion address, e.g., `http://abc123.onion`

4. Replace `YOUR_ONION_ADDRESS.onion` in `static/index.html` with your actual onion address

5. Push the updated `static/index.html` to GitHub Pages

## Accessing the Service

- The API is hosted on TOR hidden service (.onion)
- The frontend is static on GitHub Pages
- Users must access the GitHub Pages site using TOR Browser to call the .onion API
- All LLAMA API traffic is routed through TOR for anonymity

## Security

- Your own API with custom security (modify `src/app.py` for auth, rate limiting, etc.)
- TOR hidden service provides anonymity
- API key is environment variable, not exposed

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
