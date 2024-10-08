import sqlite3

import click
from flask import current_app, g

# Connection to our database file
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Allows us to pull a row
        g.db.row_factory = sqlite3.Row

    return g.db

# Closes the connection to the database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Initializing the database using the schema
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# used in python terminal, clear's all tables and start's over fresh
# click package is a terminal way to see feedback
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Registering the application
def init_app(app):
    app.teardown_appcontext(close_db) # closes database connection
    app.cli.add_command(init_db_command)