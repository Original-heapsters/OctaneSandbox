from datetime import datetime
from datetime import timedelta
import calendar
import json
import os
import urllib

# from flask import Flask
# from flask import make_response
# from flask import redirect
# from flask import request
# from flask import session
# from flask import url_for
from jose import jws
from jose import jwt
from requests.auth import HTTPBasicAuth
import jose
import requests


class oktaTest(object):


    config = None
    allowed_issuer = None
    allowed_issuers = []

    def __init__(self,config = None, allowed_issuer = None, allowed_issuers = []):
        self.config = config
        self.allowed_issuer = allowed_issuer
        self.allowed_issuers = allowed_issuers


    def setUp(self, pathToConfig = None):
        with open(pathToConfig) as config_file:
            config_json = json.load(config_file)
            self.config = config_json['oktaSample']

        # Get allowed issuer from the OKTA_ALLOWED_ISSUER environment variable,
        # use the 'oktaUrl' from our config file if that doesn't exist
        self.allowed_issuer = os.getenv('OKTA_ALLOWED_ISSUER', self.config['oidc']['issuer'])
        self.allowed_issuers.append(self.allowed_issuer)

    def fetch_jwk_for(self, id_token=None):
        if id_token is None:
            raise NameError('id_token is required')

        jwks_uri = "{}/v1/keys".format(config['oidc']['issuer'])

        unverified_header = jws.get_unverified_header(id_token)
        key_id = None
        if 'kid' in unverified_header:
            key_id = unverified_header['kid']
        else:
            raise ValueError('The id_token header must contain a "kid"')
        if key_id in public_key_cache:
            return public_key_cache[key_id]

        r = requests.get(jwks_uri)
        jwks = r.json()
        for key in jwks['keys']:
            jwk_id = key['kid']
            public_key_cache[jwk_id] = key

        if key_id in public_key_cache:
            return public_key_cache[key_id]
        else:
            raise RuntimeError("Unable to fetch public key from jwks_uri")

    
    def auth_login_redirect(self):
        return ("Redirected")


    def auth_login_custom(self):
        return ("Log in")


    def auth_callback(self,clientRequest = None):
        nonce = None
        state = None
        cookies = clientRequest.cookies
        if (('okta-oauth-nonce' in cookies) and ('okta-oauth-state' in cookies)):
            nonce = cookies['okta-oauth-nonce']
            state = cookies['okta-oauth-state']
        else:
            return "invalid nonce or state", 401
        # if (request.args.get('state') != state):
        if (clientRequest.args.get('state') != state):
            err = "'{}' != '{}'".format(
                clientRequest.args.get('state'),
                state)
            return "invalid state: {}".format(err), 401
        if 'code' not in clientRequest.args:
            return "no code in request arguments", 401

        auth = HTTPBasicAuth(self.config['oidc']['clientId'],
                             self.config['oidc']['clientSecret'])
        querystring = {
            'grant_type': 'authorization_code',
            'code': clientRequest.args.get('code'),
            'redirect_uri': self.config['oidc']['redirectUri']
        }
        url = "{}/v1/token".format(self.config['oidc']['issuer'])

        qs = "grant_type=authorization_code&code={}&redirect_uri={}".format(
            urllib.quote_plus(querystring['code']),
            urllib.quote_plus(querystring['redirect_uri'])
            )
        url = "{}/v1/token?{}".format(self.config['oidc']['issuer'], qs)
        
        headers = {
            'User-Agent': None,
            'Connection': 'close',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        r = requests.post(url,
                          # params=querystring,
                          stream=False,
                          auth=auth,
                          headers=headers)
        return_value = r.json()
        if 'id_token' not in return_value:
            return "no id_token in response from /token endpoint", 401
        id_token = return_value['id_token']

        five_minutes_in_seconds = 300
        leeway = five_minutes_in_seconds
        jwt_kwargs = {
            'algorithms': 'RS256',
            'options': {
                'verify_at_hash': False,
                # Used for leeway on the "exp" claim
                'leeway': leeway
            },
            'issuer': config['oidc']['issuer'],
            'audience': config['oidc']['clientId']
            }
        if 'access_token' in return_value:
            jwt_kwargs['access_token'] = return_value['access_token']
        try:
            jwks_with_public_key = fetch_jwk_for(id_token)
            claims = jwt.decode(
                id_token,
                jwks_with_public_key,
                **jwt_kwargs)

        except (jose.exceptions.JWTClaimsError, jose.exceptions.JWTError, jose.exceptions.JWSError, jose.exceptions.ExpiredSignatureError, NameError, sValueError):
            return (str(err), 401)
        if nonce != claims['nonce']:
            return ("invalid nonce", 401)
        # Validate 'iat' claim
        # FIXME: Open PR for moving this code here: https://git.io/v1D8M
        time_now_with_leeway = datetime.utcnow() + timedelta(seconds=leeway)
        acceptable_iat = calendar.timegm((time_now_with_leeway).timetuple())
        if 'iat' in claims and claims['iat'] > acceptable_iat:
            return ("invalid iat claim", 401)

        userSession = {
            'email': claims['email'],
            'claims': claims
            }
        return (userSession,200)
