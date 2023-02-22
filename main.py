import os
import app

# Get the environment variable
mode = os.environ.get('MODE')

if mode == 'prod':
    application = app.create_app('prod')
else:
    application = app.create_app('dev')

if __name__ == '__main__':

    if mode == 'prod':
        application.run(debug=False)
    else:
        application.run(debug=True)
