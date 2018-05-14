# Barkeep
Web repo management GUI for [homebrew app store](https://github.com/vgmoose/appstorenx) repos

## Usage

1. Install requirements:
```
pip install -r requirements.txt
```

2. Setup `./instance/config.py` to contain secret key and database login info.

3. Export the following variables:
```
export FLASK_CONFIG=development
export FLASK_APP=run.py
```

4. Setup the database (mysql db with info in #2 should be running)
```
flask db init
flask db migrate
flask db upgrade
```

5. Run it, and it should be visitable on [localhost:5000](http://localhost:5000)
```
python run.py
```

