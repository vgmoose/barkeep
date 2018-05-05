from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required

from . import home
from forms import AddRepoForm

import os, json
DATA = "./data/"

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
    repos = os.listdir(DATA)
    
    return render_template('home/dashboard.html', title="Dashboard", repos=repos)

@home.route('/dashboard/add', methods=['GET', 'POST'])
@login_required
def newrepo():
    """
    The form for making a new repo is just the folder name
    """
    form = AddRepoForm()
    if form.validate_on_submit():
        
        # make the directory for this package
        os.mkdir(DATA + form.name.data)
        
        flash('Repo created successfully')

        # redirect to the login page
        return redirect(url_for('home.dashboard'))

    # load registration template
    return render_template('home/add.html', form=form, title='Add Repo')

@home.route('/dashboard/<folder>', methods=['GET', 'POST'])
@login_required
def getrepo(folder):
    
    # check if repo doesn't exist
    if not os.path.isdir(DATA + folder):
        content = "Repo '" + folder +"' does not exist<br><br><a href='/dashboard'>Return to dashboard</a>"
        return render_template('simple.html', content=content)
    
    # load packages from json
    
    JSON = DATA + folder + "/repo.json"
    
    # touch json file if it doesn't exist
    if not os.path.exists(JSON):
        with open(JSON, 'w+') as f:
            content = {"packages": []}
            json.dump(content, f)
    
    packages = {}
    
    with open(JSON) as f:
        packages = json.load(f)
        
    if "packages" not in packages:
        packages["packages"] = []
        
    # a delete is coming in
    if request.method == 'POST' and request.form['action'] == 'delete':
        # make sure there are no packages
        if len(packages["packages"]) == 0:
            # delete the repo json and parent folder
            os.remove(JSON)
            os.rmdir(DATA + folder)
            # go back to dashboard
            return redirect(url_for("home.dashboard"))
        else:
            flash("Repo must have 0 packages to delete")
    
    return render_template('home/getrepo.html', title="%s Repo" % folder, repo=folder, packages=packages["packages"], count=len(packages["packages"]))



@home.route('/dashboard/<folder>/add', methods=['GET', 'POST'])
@login_required
def modifypackage():
    """
    The form for making or editing a new package
    """
    form = AddPackageForm()
    if form.validate_on_submit():
        
        # make the directory for this package
        os.mkdir(DATA + form.name.data)
        
        flash('Repo created successfully')

        # redirect to the login page
        return redirect(url_for('home.dashboard'))

    # load registration template
    return render_template('home/add.html', form=form, title='Add Repo')