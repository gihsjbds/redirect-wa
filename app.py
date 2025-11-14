from flask import Flask, redirect, render_template_string, request
import redis
import os
import re
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

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

def is_mobile():
    """Check if user agent is mobile device"""
    user_agent = request.headers.get('User-Agent', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone']
    return any(keyword in user_agent for keyword in mobile_keywords)

def extract_whatsapp_code(url):
    """Extract invite code from WhatsApp URL"""
    match = re.search(r'chat\.whatsapp\.com/([A-Za-z0-9]+)', url)
    return match.group(1) if match else None

@app.route('/group/<group_id>')
def redirect_group(group_id):
    if r:
        try:
            target = r.get(f'group:{group_id}')
            if target:
                target = target.decode('utf-8')
                if target.startswith('http://') or target.startswith('https://'):
                    # Handle WhatsApp links specially for mobile
                    if 'chat.whatsapp.com' in target:
                        code = extract_whatsapp_code(target)
                        if code and is_mobile():
                            # Create a simple page with big button - user must click (browsers block auto-redirect)
                            redirect_html = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Join WhatsApp Group</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
            text-align: center; 
            padding: 20px;
        }}
        .container {{ 
            background: white;
            border-radius: 20px;
            padding: 40px 30px;
            max-width: 400px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .icon {{
            width: 80px;
            height: 80px;
            background: #25D366;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
        }}
        h1 {{ color: #333; margin-bottom: 10px; font-size: 24px; }}
        p {{ color: #666; margin-bottom: 30px; font-size: 16px; }}
        .btn {{
            display: block;
            padding: 18px 30px;
            background: #25D366;
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
        }}
        .btn:active {{
            transform: scale(0.98);
        }}
        .btn-secondary {{
            background: #f0f0f0;
            color: #333;
            box-shadow: none;
        }}
        .muted {{ color: #999; font-size: 14px; margin-top: 20px; }}
        @media (max-width: 480px) {{
            .container {{ padding: 30px 20px; }}
            h1 {{ font-size: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📱</div>
        <h1>Join WhatsApp Group</h1>
        <p>Click the button below to open WhatsApp and join the group</p>
        <a href="{target}" class="btn" onclick="setTimeout(function(){{ window.location.href='{target}'; }}, 100);">Open WhatsApp</a>
        <a href="{target}" class="btn btn-secondary">Open in Browser</a>
        <p class="muted">Make sure WhatsApp is installed</p>
    </div>
    <script>
        // Auto-redirect after 3 seconds if user doesn't click
        setTimeout(function() {{
            window.location.href = "{target}";
        }}, 3000);
    </script>
</body>
</html>"""
                            return redirect_html, 200
                        else:
                            # Desktop or non-mobile: redirect to web link
                            return redirect(target, code=302)
                    else:
                        return redirect(target, code=302)
        except:
            pass
    
    return render_template_string(HTML_TEMPLATE.replace('{{ group_id }}', group_id))

@app.errorhandler(404)
def not_found(e):
    return render_template_string(HTML_TEMPLATE.replace('{{ group_id }}', 'N/A')), 404

# For Railway/production deployment
if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

