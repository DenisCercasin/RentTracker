import click
import os
import sqlite3
from flask import current_app, g

# Funktion zum Abrufen der Datenbankverbindung
def get_db_con(pragma_foreign_keys = True):
    if 'db_con' not in g: #Damit wird vermieden, dass für einen Request mehrfach eine Verbindung aufgebaut wird.
        g.db_con = sqlite3.connect(
            current_app.config['DATABASE'],#die neue Datenbank wird über Flask-Konfiguration abgerufen
            detect_types=sqlite3.PARSE_DECLTYPES #Erkennung atentypen wie Datum oder Zeit
        )
      
        g.db_con.row_factory = sqlite3.Row #für uns als Rows sichtbar 
        if pragma_foreign_keys:
            g.db_con.execute('PRAGMA foreign_keys = ON;') #Prüfung der Datenintegrität
    return g.db_con


def close_db_con(e=None):
    db_con = g.pop('db_con', None)
    if db_con is not None:
        db_con.close()

@click.command('init-db')
def init_db():
    try:
        #hier wird Speicherung von Flask Konfigurationen und z. B. die SQLite-Datenbank
        os.makedirs(current_app.instance_path)
    except OSError:
        pass
    db_con = get_db_con()
    with current_app.open_resource('sql/drop_tables.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    with current_app.open_resource('sql/create_tables.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    click.echo('Database has been initialized.')

def insert_sample():
    db_con = get_db_con()
    with current_app.open_resource("sql/insert_sample.sql") as f:
        db_con.executescript(f.read().decode("utf8"))