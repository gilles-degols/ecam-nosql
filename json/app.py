import os
import flask
import werkzeug
from flask_openapi3 import OpenAPI, Info

info = Info(title="API", version="0.1.0")
app = OpenAPI("Ecam", info=info)
app.secret_key = os.environ.get("API_SECRET", "something-secret")

from customer import api

app.register_api_view(api)

# flask run --debug
# python3 -m flask run --debug