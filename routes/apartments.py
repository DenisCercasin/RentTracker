from flask import Blueprint, render_template

apartments_bp = Blueprint ("apartments", __name__)

@apartments_bp.route("/apartments")
def list_apartments():
    #function to fetch all apartments and then show it in a table
    return render_template("apartments.html")
