import os
import app

if __name__ == '__main__':

    # Get the environment variable
    mode = os.environ.get('MODE')

    if mode == 'prod':
        application = app.create_app('prod')
        application.run(debug=False)
    else:
        application = app.create_app('dev')
        application.run(debug=True)
