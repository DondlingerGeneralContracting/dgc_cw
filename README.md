# 🍒 Cherri Generator

AI-powered Siri Shortcuts code generator using the official Llama API (`api.llama.com`).

## What is Cherri?

[Cherri](https://cherrilang.org) compiles to Siri Shortcuts. Describe what you want, get working code.

## Stack

- **Frontend**: Mobile-first PWA (add to home screen)
- **Backend**: Flask on Raspberry Pi
- **AI**: Llama-4-Scout-17B-16E-Instruct-FP8 via `api.llama.com`
- **Network**: Tailscale + Tor hidden service

## Deploy to Raspberry Pi

```bash
# SSH to Pi via Tailscale
ssh jdd@100.x.x.x

# Clone
git clone https://github.com/DondlingerGeneralContracting/dgc_cw.git
cd dgc_cw

# Ensure .chameleon.environment is present (contains API keys)
# Run with Docker
cd docker
docker-compose up -d --build
```

## Access

| Method       | URL                                              |
| ------------ | ------------------------------------------------ |
| Tailscale    | `http://100.x.x.x:5000`                          |
| Tor          | Check `docker logs tor-proxy` for .onion address |
| GitHub Pages | Static frontend only (needs backend)             |

## Get Your .onion Address

```bash
docker exec -it dgc_cw-tor-proxy-1 cat /var/lib/tor/hidden_service/hostname
```

## API Endpoints

```
POST /api/generate  { "prompt": "..." } → { "code": "...", "success": true }
POST /api/explain   { "code": "..." }   → { "explanation": "...", "success": true }
```

## Local Dev

```bash
export LLAMA_API_KEY="your_key"
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`

## Resources

- [Cherri Docs](https://cherrilang.org/language/)
- [Cherri Playground](https://playground.cherrilang.org/)
- [Llama API](https://llama.com)

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
