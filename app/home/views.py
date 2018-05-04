from flask import render_template
from flask_login import login_required

from . import home

import os

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Home")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    
    # get the directories in the data folder
    # (each directory represents another repo)
    repos = os.listdir("./data")
    
    return render_template('home/dashboard.html', title="Dashboard", repos=repos)
