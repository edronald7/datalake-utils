# run.py
# This script runs the Flask application. It should be run to start the server.
# Make sure to run this script in the same environment where your Flask app is running.
# Usage: python run.py 

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)