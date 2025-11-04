from flask import Flask, redirect, render_template_string
import redis
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Redis connection
redis_url = os.getenv('REDIS_URL')
if redis_url:
    r = redis.from_url(redis_url)
else:
    r = None

# Fallback HTML template
HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Join the WhatsApp group</title>
    <style>
        body { margin: 0; background: #0b1220; color: #fff; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; }
        .container { max-width: 640px; margin: 0 auto; padding: 40px 16px; }
        .card { background: #0f172a; border: 1px solid #1f2a44; border-radius: 12px; padding: 24px; }
        .title { font-size: 24px; margin: 0 0 8px 0; }
        .subtitle { opacity: 0.8; margin: 0 0 16px 0; }
        .buttons { display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0 24px 0; }
        .btn { display: inline-block; padding: 10px 14px; border-radius: 8px; text-decoration: none; color: white; border: 1px solid #1f2a44; }
        .btn.primary { background: #22c55e; border-color: #16a34a; }
        .muted { opacity: 0.6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1 class="title">Join the WhatsApp group</h1>
            <p class="subtitle">Trying to open WhatsApp...</p>
            <div class="buttons">
                <a class="btn primary" href="https://web.whatsapp.com" target="_blank" rel="noopener noreferrer">Open in browser</a>
                <a class="btn" href="whatsapp://" rel="noopener noreferrer">Open WhatsApp</a>
            </div>
            <p class="muted">If nothing works, follow the steps below.</p>
            <ol class="muted">
                <li>Ensure WhatsApp is installed.</li>
                <li>Ask the admin to set a target for group ID {{ group_id }}.</li>
            </ol>
        </div>
    </div>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE.replace('{{ group_id }}', 'N/A'))

@app.route('/group/<group_id>')
def redirect_group(group_id):
    if r:
        try:
            target = r.get(f'group:{group_id}')
            if target:
                target = target.decode('utf-8')
                if target.startswith('http://') or target.startswith('https://'):
                    return redirect(target, code=302)
        except:
            pass
    
    return render_template_string(HTML_TEMPLATE.replace('{{ group_id }}', group_id))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    # Disable debug in production
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

