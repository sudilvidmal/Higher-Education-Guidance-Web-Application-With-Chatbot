from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from app import app as main_app
from linkedinInt import linkedin_app

# Define the WSGI application
application = DispatcherMiddleware(main_app, {
    '/linkedin': linkedin_app
})

if __name__ == '__main__':
    # Run the application using run_simple from werkzeug
    run_simple('127.0.0.1', 5000, application, use_reloader=True)
