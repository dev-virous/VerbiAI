from flask import *
import os

desired_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
print(desired_root_path)

routes = Flask(
    __name__,
    root_path=desired_root_path
)