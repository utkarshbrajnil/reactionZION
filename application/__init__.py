"""Initialize Flask app."""
from flask import Flask
import sqlite3



def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import Flask routes

        from application import reaction

        # Import Dash application
        from application.plotlydash.dashboard import create_dashboard
        conn = sqlite3.connect('data/alldata.db', isolation_level=None, check_same_thread=False)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, comments TEXT, sentiment REAL)")
        app = create_dashboard(app)

        # Compile CSS
        if app.config['FLASK_ENV'] == 'development':
            from application.assets import compile_assets
            compile_assets(app)

        return app
