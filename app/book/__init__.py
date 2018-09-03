from flask import Blueprint

book = Blueprint('book', __name__, template_folder='templates')

from . import views
from . import models


