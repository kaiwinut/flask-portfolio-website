from flask import Blueprint, render_template

homepage = Blueprint('homepage', __name__)

@homepage.route('/')
@homepage.route('/home/')
def home():
    from server.config import CURRENT_YEAR
    return render_template('index.html', current_year=CURRENT_YEAR)