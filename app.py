from flask import Flask, Blueprint, render_template
from routes.apartments import apartments_bp
from routes.tenants import tenants_bp
import os,db

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'rent_tracker.sqlite')
)

app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con)



app.register_blueprint(apartments_bp)
app.register_blueprint(tenants_bp)


@app.route("/")
def index():
    return render_template("base.html")

@app.route("/insert/sample")
def run_insert_sample():
    db.insert_sample()
    return "Database flushed and populated with more sample data"


