

Set PYTHONPATH config variable under Settings > Config Variables `PYTHONPATH=/app/src/`

Add python support `heroku buildpacks:add --index 1 heroku/python -a your_app_name`

Add nodejs support to run 'bower install' during build `heroku buildpacks:add --index 1 heroku/nodejs -a your_app_name`

Set WEB_CONCURRENCY config variable `WEB_CONCURRENCY=3`