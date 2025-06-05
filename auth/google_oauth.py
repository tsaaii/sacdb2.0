"""
auth/google_oauth.py - OAuth without hardcoded fallback

This version only loads emails from the config file to test proper file loading.
"""

import os
import json
import secrets
from functools import wraps
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import flask
from flask import session, request, redirect, jsonify

class GoogleOAuth:
    def __init__(self, app=None):
        self.app = app
        self.allowed_emails = set()
        self.client_secrets_file = 'client_secrets.json'
        self.flow = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize Google OAuth with your Flask app"""
        self.app = app
        
        if not app.secret_key:
            app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))
        
        self.load_allowed_emails()
        self.setup_oauth_flow()
        self.register_routes()
    
    def load_allowed_emails(self):
        """Load allowed emails ONLY from config file - no hardcoded fallback"""
        
        config_file = 'config/allowed_emails.json'
        
        print(f"\n📧 Loading allowed emails from config file only...")
        print(f"   Config file: {config_file}")
        print(f"   File exists: {os.path.exists(config_file)}")
        
        # Start with empty set - NO hardcoded emails
        self.allowed_emails = set()
        
        if not os.path.exists(config_file):
            print(f"   ❌ Config file does not exist!")
            print(f"   Creating default config file...")
            self.create_config_file(config_file)
        
        try:
            with open(config_file, 'r') as f:
                content = f.read().strip()
                print(f"   File content preview: {content[:100]}...")
                
            if not content:
                print(f"   ❌ Config file is empty!")
                self.create_config_file(config_file)
                # Re-read the file after creating it
                with open(config_file, 'r') as f:
                    content = f.read().strip()
            
            # Parse JSON
            config = json.loads(content)
            file_emails = config.get('allowed_emails', [])
            
            print(f"   Raw emails from config: {file_emails}")
            
            # Process emails
            for email in file_emails:
                if email and email.strip():
                    clean_email = email.strip().lower()
                    self.allowed_emails.add(clean_email)
                    print(f"   ✅ Added: '{email}' -> '{clean_email}'")
            
            if not self.allowed_emails:
                print(f"   ⚠️  No valid emails found in config file!")
                print(f"   Creating default config with your email...")
                self.create_config_file(config_file)
                # Try to load again
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    for email in config.get('allowed_emails', []):
                        if email and email.strip():
                            self.allowed_emails.add(email.strip().lower())
                
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON decode error: {e}")
            print(f"   Recreating config file with correct format...")
            self.create_config_file(config_file)
            # Try to load the recreated file
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    for email in config.get('allowed_emails', []):
                        if email and email.strip():
                            self.allowed_emails.add(email.strip().lower())
            except:
                print(f"   ❌ Still cannot load config file!")
                
        except Exception as e:
            print(f"   ❌ Error reading config file: {e}")
            print(f"   Will try to create a new one...")
            self.create_config_file(config_file)
        
        print(f"\n📊 Final Results:")
        print(f"   Total emails loaded: {len(self.allowed_emails)}")
        if self.allowed_emails:
            print(f"   ✅ Authorized emails:")
            for email in sorted(self.allowed_emails):
                print(f"      - {email}")
        else:
            print(f"   ❌ NO EMAILS LOADED - Authorization will fail!")
            print(f"   Check your config file: {config_file}")
    
    def create_config_file(self, config_file):
        """Create a properly formatted config file"""
        try:
            os.makedirs('config', exist_ok=True)
            
            config = {
                "allowed_emails": [
                    "saaitejaa@gmail.com",
                    "admin@advitialabs.com"
                ]
            }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"   ✅ Created config file: {config_file}")
            print(f"   Default emails: {config['allowed_emails']}")
            
        except Exception as e:
            print(f"   ❌ Could not create config file: {e}")
    
    def setup_oauth_flow(self):
        """Setup Google OAuth2 flow"""
        try:
            # For development only
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
            
            base_url = os.getenv('BASE_URL', 'http://localhost:8080')
            redirect_uri = f"{base_url}/auth/callback"
            
            scopes = [
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'
            ]
            
            self.flow = Flow.from_client_secrets_file(
                self.client_secrets_file,
                scopes=scopes,
                redirect_uri=redirect_uri
            )
            print("✅ Google OAuth flow configured successfully")
            
        except FileNotFoundError:
            print("❌ client_secrets.json not found")
            self.flow = None
        except Exception as e:
            print(f"❌ OAuth setup error: {e}")
            self.flow = None
    
    def register_routes(self):
        """Register OAuth routes"""
        
        @self.app.route('/auth/login')
        def oauth_login():
            if not self.flow:
                return jsonify({'error': 'OAuth not configured'}), 500
            
            authorization_url, state = self.flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='select_account'
            )
            
            session['oauth_state'] = state
            print(f"✅ Redirecting to Google OAuth...")
            return redirect(authorization_url)
        
        @self.app.route('/auth/callback')
        def oauth_callback():
            if not self.flow:
                return redirect('/?error=oauth_not_configured')
            
            if session.get('oauth_state') != request.args.get('state'):
                print("❌ OAuth state mismatch")
                return redirect('/?error=invalid_state')
            
            try:
                self.flow.fetch_token(authorization_response=request.url)
                credentials = self.flow.credentials
                
                request_session = requests.Request()
                id_info = id_token.verify_oauth2_token(
                    credentials.id_token,
                    request_session,
                    self.flow.client_config['client_id']
                )
                
                # Get user info
                user_email_raw = id_info.get('email', '')
                user_email = user_email_raw.strip().lower()
                user_name = id_info.get('name', '')
                
                print(f"\n🔐 OAuth Callback (Config File Only):")
                print(f"   Raw email: '{user_email_raw}'")
                print(f"   Cleaned email: '{user_email}'")
                print(f"   Name: '{user_name}'")
                
                print(f"\n🔍 Authorization Check (No Hardcoded Fallback):")
                print(f"   User email: '{user_email}'")
                print(f"   Config file emails: {sorted(list(self.allowed_emails))}")
                print(f"   Email count from file: {len(self.allowed_emails)}")
                print(f"   Is authorized: {user_email in self.allowed_emails}")
                
                if user_email in self.allowed_emails:
                    print(f"✅ ACCESS GRANTED (from config file): {user_email}")
                    
                    session['user'] = {
                        'id': id_info.get('sub'),
                        'email': user_email,
                        'name': user_name or user_email.split('@')[0],
                        'picture': id_info.get('picture'),
                        'authenticated': True,
                        'auth_method': 'google_oauth'
                    }
                    
                    return redirect('/main')
                else:
                    print(f"❌ ACCESS DENIED (not in config file): {user_email}")
                    if not self.allowed_emails:
                        print(f"   Problem: No emails loaded from config file!")
                        print(f"   Check: config/allowed_emails.json")
                    else:
                        print(f"   To fix: Add '{user_email}' to config/allowed_emails.json")
                    session.clear()
                    return redirect('/?error=unauthorized_email')
                
            except Exception as e:
                print(f"❌ OAuth callback error: {e}")
                import traceback
                traceback.print_exc()
                session.clear()
                return redirect('/?error=auth_failed')
        
        @self.app.route('/auth/logout')
        def oauth_logout():
            user_email = session.get('user', {}).get('email', 'Unknown')
            session.clear()
            print(f"✅ User {user_email} logged out")
            return redirect('/')
        
        @self.app.route('/auth/status')
        def auth_status():
            user = session.get('user')
            if user and user.get('authenticated'):
                return jsonify({
                    'authenticated': True,
                    'user': {
                        'email': user.get('email'),
                        'name': user.get('name'),
                        'picture': user.get('picture')
                    }
                })
            return jsonify({'authenticated': False})
        
        @self.app.route('/auth/debug')
        def auth_debug():
            """Debug endpoint to check configuration"""
            return jsonify({
                'oauth_configured': self.flow is not None,
                'client_secrets_exists': os.path.exists(self.client_secrets_file),
                'allowed_emails_from_file': sorted(list(self.allowed_emails)),
                'allowed_emails_count': len(self.allowed_emails),
                'config_file_exists': os.path.exists('config/allowed_emails.json'),
                'session_user': session.get('user', {}),
                'is_authenticated': self.is_authenticated(),
                'config_file_readable': self.test_config_file()
            })
        
        def test_config_file():
            """Test if config file can be read"""
            try:
                with open('config/allowed_emails.json', 'r') as f:
                    config = json.load(f)
                return {'status': 'readable', 'emails': config.get('allowed_emails', [])}
            except Exception as e:
                return {'status': 'error', 'error': str(e)}
    
    def is_authenticated(self):
        user = session.get('user')
        return user is not None and user.get('authenticated', False)
    
    def get_current_user(self):
        return session.get('user')

# Global instance
oauth = GoogleOAuth()

def init_oauth(app):
    oauth.init_app(app)
    return oauth

def is_authenticated():
    return oauth.is_authenticated()

def get_current_user():
    return oauth.get_current_user()