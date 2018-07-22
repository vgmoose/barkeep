# Barkeep
Web repo management GUI for [homebrew app store](https://github.com/vgmoose/appstorenx) repos

## Usage
1. If you have any existing repos, place them as whole folders within the `./data` folder. This will be shared with the containers and persistent on disk.

2. Use docker-compose to get it running on [localhost:5000](http://localhost:5000).
```
docker-compose start
```

This should bring up two containers, one volume for persisting the mysql database, and the other for running the server. See below for first time setup info.

## First-time Setup
Before running for the first time, you need to build and the barkeep container and set up the mysql database tables.

1. Create barkeep container
```
docker-compose build
```

2. Bring up mysql container and run db migration script
```
docker-compose start mysql
docker-compose run barkeep sh migrations.sh
```

The mysql container should now be setup and you can bring up the `barkeep` container as described in Usage.
