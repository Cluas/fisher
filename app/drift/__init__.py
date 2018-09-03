from flask import Blueprint

drift = Blueprint('drift', __name__, url_prefix='/drift', template_folder='templates')

from . import views
from . import models


