# Redirect WA - Python Edition

Simple Python redirect service with Telegram bot control. Create links like `/group/3` and change their destination via Telegram.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get Redis URL (choose one):**

   **Option A: Upstash (Recommended - Free & Easy)**
   - Go to https://upstash.com and sign up (free)
   - Click "Create Database" → Choose region → Create
   - Click on your database → Go to "Redis" tab
   - Copy the "Endpoint" URL (looks like: `redis://default:xxxxx@xxxxx.upstash.io:6379`)
   - That's your `REDIS_URL`!

   **Option B: Redis Cloud (Free tier)**
   - Go to https://redis.com/cloud and sign up
   - Create a free database
   - Copy the connection URL from the dashboard

   **Option C: Local Redis (for testing only)**
   - Install Redis on your computer
   - Use: `redis://localhost:6379`

3. **Create Telegram Bot:**
   - Message @BotFather on Telegram
   - Create new bot and copy the token

4. **Set environment variables:**

   You can put these in a `.env` file in the project root and both `app.py` and `bot.py` will read them automatically.

   **.env example:**
   ```env
   REDIS_URL=rediss://default:YOUR_PASSWORD@true-snipe-27040.upstash.io:6379
   TELEGRAM_BOT_TOKEN=123:ABC-your-token
   ADMIN_CHAT_ID=123456789
   PUBLIC_BASE_URL=https://your-domain.vercel.app
   PORT=3000
   ```

   Or set them in your shell:

   **On Windows (PowerShell):**
   ```powershell
   $env:REDIS_URL="redis://default:your-password@your-host.upstash.io:6379"
   $env:TELEGRAM_BOT_TOKEN="123:ABC-your-token"
   $env:ADMIN_CHAT_ID="123456789"  # Optional
   $env:PUBLIC_BASE_URL="https://your-domain.vercel.app"
   $env:PORT="3000"
   ```

   **On Mac/Linux:**
   ```bash
   export REDIS_URL="redis://default:your-password@your-host.upstash.io:6379"
   export TELEGRAM_BOT_TOKEN="123:ABC-your-token"
   export ADMIN_CHAT_ID="123456789"  # Optional
   export PUBLIC_BASE_URL="https://your-domain.vercel.app"
   export PORT=3000
   ```

   **Example REDIS_URL from Upstash:**
   ```
   redis://default:AbCdEf123456@us1-cool-redis-12345.upstash.io:6379
   ```
   (If your Upstash shows a redis-cli command like `redis-cli --tls -u redis://...`, convert it to `rediss://...` and use that as `REDIS_URL`.)

5. **Run the app:**
```bash
python app.py
```

6. **Run the bot (in another terminal):**
```bash
python bot.py
```

## Usage

**Telegram Bot Commands:**
- `/set 3 https://chat.whatsapp.com/yourInviteLink` - Set redirect
- `/get 3` - Get current target
- `/del 3` - Delete mapping

**Visit:**
- `http://localhost:3000/group/3` - Redirects to stored URL
- If no mapping, shows fallback page

## Deploy to Hosting (Free Alternatives)

### Option 1: Railway.app (Recommended - Easiest)

1. Go to https://railway.app and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and deploys
5. Go to "Variables" tab and add:
   - `REDIS_URL` (your Upstash Redis URL)
   - `TELEGRAM_BOT_TOKEN` (your bot token)
   - `ADMIN_CHAT_ID` (optional)
   - `PUBLIC_BASE_URL` (will be `https://your-app.railway.app` - Railway gives you this)
   - `PORT` (Railway sets this automatically, but you can set `3000` if needed)
6. Your app will be live at: `https://your-app.railway.app`
7. **Static URL:** Railway gives you a permanent URL like `https://redirect-wa-production.up.railway.app` that never changes!

**To get your static URL:**
- After deployment, go to Settings → Generate Domain
- You can also use a custom domain (free)

---

### Option 2: Render.com (Free Tier)

1. Go to https://render.com and sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - **Name:** `redirect-wa` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. Add Environment Variables:
   - `REDIS_URL`
   - `TELEGRAM_BOT_TOKEN`
   - `ADMIN_CHAT_ID` (optional)
   - `PUBLIC_BASE_URL` (will be `https://redirect-wa.onrender.com`)
   - `PORT` (Render sets this automatically via `PORT` env var)
6. Click "Create Web Service"
7. Your app will be live at: `https://redirect-wa.onrender.com`
8. **Static URL:** Render gives you a permanent `*.onrender.com` URL that stays the same!

**Note:** Free tier may spin down after 15 min inactivity, but it's free!

---

### Option 3: Fly.io (Free Tier)

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup`
3. Create app: `fly launch` (follow prompts)
4. Set secrets:
   ```bash
   fly secrets set REDIS_URL="your-redis-url"
   fly secrets set TELEGRAM_BOT_TOKEN="your-token"
   fly secrets set PUBLIC_BASE_URL="https://your-app.fly.dev"
   ```
5. Deploy: `fly deploy`
6. Your app: `https://your-app.fly.dev`

---

### Option 4: Vercel (Original)

1. Create `vercel.json` (already included in repo)
2. Push to GitHub
3. Import project in Vercel dashboard
4. Set environment variables
5. Deploy

---

### Running the Telegram Bot

The bot needs to run separately (not on the hosting platform). Options:

**Option A: Run on your computer (always on)**
- Just run `python bot.py` on your PC
- Keep terminal open

**Option B: Run on Railway/Render (separate service)**
- Create a second service for `bot.py`
- Set start command: `python bot.py`
- Add same environment variables

**Option C: Use a VPS (DigitalOcean, Linode - $5/month)**
- Deploy bot.py there
- Runs 24/7

---

## Quick Start Summary

1. **Deploy web app** → Railway/Render (free static URL)
2. **Run Telegram bot** → Your computer or separate service
3. **Set redirects** → Use `/set` command in Telegram bot
4. **Share links** → `https://your-static-url.com/group/3`
