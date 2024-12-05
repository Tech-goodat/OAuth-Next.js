from flask import Flask, jsonify,redirect, url_for, session, request
from flask_restful import Api, Resource
from authlib.integrations.flask_client import OAuth

app=Flask(__name__)
app.secret_key = 'your_secret_key'
oauth = OAuth(app)
api=Api(app)

google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

class Index(Resource):
    def get(self):
        return jsonify({"message":"welcome to OAuth test page"})
    
api.add_resource(Index, "/")

class GoogleLogin(Resource):
    def get(self):
        redirect_uri = request.url_root + 'authorize'
        return redirect(google.authorize_redirect(redirect_uri))
    
class GoogleAuthorize(Resource):
    def get(self):
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)
        # Here you would create or find the user in your database
        return jsonify({
            "message": "User authenticated",
            "user": user_info,
            "token": token  # Optionally return a token to the client
        })
    
api.add_resource(GoogleLogin, '/login')
api.add_resource(GoogleAuthorize, '/authorize')

if __name__=="__main__":
    app.run(port=5555, debug=True)