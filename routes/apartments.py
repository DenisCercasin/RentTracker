from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import get_db_con
from flask_login import current_user

apartments_bp = Blueprint ("apartments", __name__)

@apartments_bp.route("/apartments", methods = ["GET", "POST"])
def list_apartments():
    conn = get_db_con()
    if request.method=="POST":
        return redirect(url_for("apartments.create_apartment"))
    
    apartments = conn.execute('SELECT * FROM apartment WHERE user_id = ?', (current_user.id,)).fetchall()
    conn.close()
    #function to fetch all apartments and then show it in a table
    print("hello")
    return render_template("apartments.html", apartments = apartments)

@apartments_bp.route("/apartments/edit/<int:id>", methods=["GET", "POST"])
def edit_apartment(id):
    db_con = get_db_con()
    
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        db_con.execute("UPDATE apartment SET name = ?, address = ? WHERE id = ? AND user_id = ?", (name, address, id, current_user.id))
        db_con.commit()
        flash("Apartment updated successfully.")
        return redirect(url_for("apartments.list_apartments"))
    
    apartment = db_con.execute("SELECT * FROM apartment WHERE id = ? AND user_id = ?", (id, current_user.id)).fetchone() # needs a tuple!
    return render_template("edit_apartment.html", apartment=apartment)

@apartments_bp.route("/apartments/delete/<int:id>", methods=["GET", "POST"])
def delete_apartment(id):
    db_con = get_db_con()
    if request.method=="POST":
        db_con.execute("DELETE FROM apartment WHERE id = ? AND user_id = ?",(id, current_user.id))
        db_con.commit()
        flash("Success")
        return redirect(url_for("apartments.list_apartments"))
    
    apartment = db_con.execute("SELECT * FROM apartment WHERE id = ? AND user_id = ?", (id,current_user.id)).fetchone()
    return render_template("delete_apartment.html", apartment = apartment)

@apartments_bp.route("/apartments/create", methods=["GET", "POST"])
def create_apartment():
    if request.method=="GET":
        return render_template("create_apartment.html")
    else:
        db_con = get_db_con()
        apartment_name = request.form["name"]
        apartment_address = request.form["address"]
        db_con.execute("INSERT INTO apartment (address,name, user_id) VALUES (?,?,?)", (apartment_address, apartment_name, current_user.id))
        db_con.commit()
        return redirect(url_for("apartments.list_apartments"))