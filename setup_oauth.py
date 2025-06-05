"""
auth/google_oauth.py - Final Fixed Google OAuth Integration

This version properly loads and checks allowed emails.
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
        """Load allowed emails from config file with enhanced debugging"""
        config_file = 'config/allowed_emails.json'
        
        print(f"\n📧 Loading allowed emails from: {config_file}")
        print(f"   File exists: {os.path.exists(config_file)}")
        
        try:
            # Check if file exists
            if not os.path.exists(config_file):
                print(f"   ❌ Config file does not exist!")
                # Create the config file
                os.makedirs('config', exist_ok=True)
                default_config = {
                    "allowed_emails": [

                    ]
                }
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                print(f"   ✅ Created default config file with your email")
                self.allowed_emails = set(default_config['allowed_emails'])
            else:
                # File exists, try to read it
                with open(config_file, 'r') as f:
                    content = f.read()
                    print(f"   File content: {content[:200]}...")
                    
                config = json.loads(content)
                raw_emails = config.get('allowed_emails', [])
                
                print(f"   Raw emails from file: {raw_emails}")
                
                # Clean and store emails
                self.allowed_emails = set()
                for email in raw_emails:
                    clean_email = email.strip().lower()
                    self.allowed_emails.add(clean_email)
                    print(f"   Added email: '{email}' -> '{clean_email}'")
            
            print(f"✅ Loaded {len(self.allowed_emails)} allowed emails:")
            for email in sorted(self.allowed_emails):
                print(f"   - {email}")
                
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON decode error: {e}")
            self.allowed_emails = set()
        except Exception as e:
            print(f"   ❌ Error loading emails: {e}")
            self.allowed_emails = set()
    
    def setup_oauth_flow(self):
        """Setup Google OAuth2 flow"""
        try:
            # For development only
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
            
            base_url = os.getenv('BASE_URL', 'http://localhost:8080')
            redirect_uri = f"{base_url}/auth/callback"
            
            # Use full scope URLs to avoid scope change errors
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
                
                print(f"\n🔐 OAuth Callback:")
                print(f"   Raw email: '{user_email_raw}'")
                print(f"   Cleaned email: '{user_email}'")
                print(f"   Name: '{user_name}'")
                
                print(f"\n🔍 Checking email authorization:")
                print(f"   User email: '{user_email}'")
                print(f"   Allowed emails: {sorted(list(self.allowed_emails))}")
                print(f"   Email in allowed list: {user_email in self.allowed_emails}")
                
                if user_email in self.allowed_emails:
                    print(f"✅ Email authorized: {user_email}")
                    
                    session['user'] = {
                        'id': id_info.get('sub'),
                        'email': user_email,
                        'name': user_name or user_email.split('@')[0],
                        'picture': id_info.get('picture'),
                        'authenticated': True,
                        'auth_method': 'google_oauth'
                    }
                    
                    print(f"✅ User {user_email} logged in successfully")
                    return redirect('/main')
                else:
                    print(f"❌ Email NOT authorized: {user_email}")
                    print(f"   Available emails: {sorted(list(self.allowed_emails))}")
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
                'allowed_emails': sorted(list(self.allowed_emails)),
                'allowed_emails_count': len(self.allowed_emails),
                'config_file_exists': os.path.exists('config/allowed_emails.json'),
                'session_user': session.get('user', {}),
                'is_authenticated': self.is_authenticated()
            })
    
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