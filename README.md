# LLAMA Chat Interface with Netlify Proxy

Interactive web interface for chatting with LLAMA AI models using Netlify Functions as a universal proxy.

## Netlify Setup

The API calls are proxied through your Netlify function at:
`https://llama-universal-netlify-project.netlify.app/.netlify/functions/llama-proxy`

### Deploy Static Frontend

1. The `static/index.html` is updated to call the Netlify proxy
2. Push to GitHub and enable GitHub Pages
3. Access at: https://dondlingergeneralcontracting.github.io/dgc_cw/

### Netlify Function Details

- Endpoint: `/.netlify/functions/llama-proxy`
- Query param: `?path=/chat/completions`
- Body: Standard LLAMA API request
- Response: Proxied LLAMA response

## Alternative: Docker on Raspberry Pi

If you prefer local deployment, the Docker setup is still available for your Pi on Tailnet.

### Setup on Raspberry Pi

1. **SSH to your Pi as user jdd**:
   ```bash
   ssh jdd@your-pi-tailscale-ip
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/DondlingerGeneralContracting/dgc_cw.git
   cd dgc_cw
   export LLAMA_API_KEY="your_actual_key"
   export LLAMA_API_URL="https://api.llama.com/v1/chat/completions"
   ```

3. **Run the container**:
   ```bash
   cd docker
   docker-compose up -d --build
   ```

4. **Access**: API at `http://your-pi-tailscale-ip:5000/api/chat`

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
