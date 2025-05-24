from flask import Blueprint, render_template

tenants_bp = Blueprint ("tenants", __name__)

@tenants_bp.route("/tenants")
def list_tenants():
    #function to fetch all tenants and then show it in a table
    return render_template("tenants.html")
