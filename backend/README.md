# Raspberry Pi Backend Setup

1. Install dependencies on your Raspberry Pi:
   ```
   sudo apt update
   sudo apt install python3 python3-pip tor
   ```

2. Clone or copy the backend code to your Pi:
   - Copy `backend/app.py` and `backend/requirements.txt` to your Pi.

3. Install Python packages:
   ```
   pip3 install -r requirements.txt
   ```

4. Set environment variables:
   - Create a `.env` file or export: `export LLAMA_API_KEY=your_key_here`

5. Configure Tor:
   - Tor should be installed and running: `sudo systemctl start tor`
   - Ensure it's listening on 127.0.0.1:9050

6. Run the Flask app:
   ```
   python3 app.py
   ```

7. Set up Tailscale funnel for public access:
   - Install Tailscale on Pi if not already.
   - Run: `tailscale funnel 5000`
   - Get the public URL (e.g., https://pi-name.ts.net)

8. Update `index.html` on the frontend with the funnel URL.

9. Deploy the frontend to GitHub Pages as before.

The backend will use Tor for all outgoing requests to DDGS and LLaMA API for security.