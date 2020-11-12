from django.contrib.auth import authenticate

import json
import jwt
import requests
import os


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_IDENTIFIER = os.getenv("AUTH0_IDENTIFIER")


def jwt_get_username_from_payload_handler(payload):
    username = payload.get("sub").replace("|", ".")
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):

    header = jwt.get_unverified_header(token)
    jwks = requests.get("https://{}/.well-known/jwks.json".format(AUTH0_DOMAIN)).json()
    public_key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception("Public key not found.")

    issuer = "https://{}/".format(AUTH0_DOMAIN)
    return jwt.decode(
        token,
        public_key,
        audience=AUTH0_IDENTIFIER,
        issuer=issuer,
        algorithms=["RS256"],
    )


def get_user_info(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]
    endpoint = "https://{}/userinfo".format(AUTH0_DOMAIN)
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(endpoint, headers=headers)
    json = response.json()
    print("response:" + str(response))
    return json