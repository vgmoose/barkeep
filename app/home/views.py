from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required

from . import home
from forms import AddRepoForm, AddPackageForm

from collections import defaultdict

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

    for repo in repos:
        # remove it if it's not a directory
        if not os.path.isdir(DATA + repo):
            repos.remove(repo)

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
    return render_template('home/add.html', form=form, title='Local Repo', target="add")

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

        # make packages directory
        os.mkdir(DATA + folder + "/packages")

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



@home.route('/dashboard/<folder>/<package>', methods=['GET', 'POST'])
@login_required
def modifypackage(folder, package):
    """
    The form for making or editing a new package
    """
    form = AddPackageForm()

    # if it's not "add", we should try to load an existing package
    if package != "add":
        INFO_PATH = DATA + folder + "/packages/" + package + "/info.json"

        # try to open the file
        try:
            with open(INFO_PATH, "r") as inp:
                d = json.load(inp)
                contents = defaultdict(str, d)

                # read in all properties
                form.name.data       = package
                form.name.render_kw = {'disabled':''}
                form.title.data      = contents["title"]
                form.author.data     = contents["author"]
                form.category.data   = contents["category"]
                form.version.data    = contents["version"]
                form.short_desc.data = contents["description"]
                form.details.data    = contents["details"].replace("\\n", "\n")
                form.url.data        = contents["url"]
                form.license.data    = contents["license"]
        except IOError:
            return render_template('404.html', resource=package), 404

    if form.validate_on_submit():

        # make the directory for this package
        PKG_PATH = DATA + folder + "/" + form.name.data + "/"
        os.mkdir(PKG_PATH)

        flash('Package created successfully')

        # redirect to the login page
        return redirect(url_for('home.dashboard'))

    # load registration template
    return render_template('home/add.html', form=form, title='Package', target=package)
