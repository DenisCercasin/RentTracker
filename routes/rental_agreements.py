from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import get_db_con
from flask_login import current_user

rental_agreements_bp = Blueprint ("rental_agreements", __name__)

@rental_agreements_bp.route("/rental_agreements", methods = ["GET", "POST"])
def list_rental_agreements():
    conn = get_db_con()
    if request.method=="POST":
        return redirect(url_for("rental_agreements.create_rental_agreement"))

    rental_agreements = conn.execute("""
        SELECT
        ra.id,
        ra.apartment_id,
        ra.tenant_id,
        a.name AS apartment_name,
        t.name AS tenant_name,
        ra.start_date,
        ra.end_date,
        ra.rent_amount
        FROM rental_agreement ra
        JOIN apartment a ON ra.apartment_id = a.id
        JOIN tenant t ON ra.tenant_id = t.id
        WHERE ra.user_id = ?
        """, (current_user.id,)).fetchall()
    conn.close()
    #function to fetch all apartments and then show it in a table
    return render_template("rental_agreements.html", rental_agreements = rental_agreements)


@rental_agreements_bp.route("/rental_agreements/edit/<int:id>", methods = ["GET", "POST"])
def edit_rental_agreement(id):
    db_con = get_db_con()
    if request.method=="GET":
        # Get current agreement
        agreement = db_con.execute("""
            SELECT * FROM rental_agreement WHERE id = ? AND user_id = ?
        """, (id, current_user.id)).fetchone()

        # Get options for dropdowns
        apartment = db_con.execute("SELECT id, name FROM apartment WHERE id = ? AND user_id", (id, current_user.id)).fetchone()
        tenants = db_con.execute("SELECT id, name FROM tenant WHERE user_id = ?", (current_user.id)).fetchall()

        return render_template("edit_rental_agreement.html", agreement=agreement,
                            apartment=apartment, tenants=tenants)
    
    else:
        tenant_id = request.form["tenant"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        rent_amount = request.form["rent_amount"]
        db_con.execute("UPDATE rental_agreement SET tenant_id = ?, start_date = ?, end_date = ?, rent_amount = ? WHERE id = ? AND user_id = ?", (tenant_id, start_date, end_date, rent_amount, id, current_user.id))
        db_con.commit()
        flash("Rental agreement updated successfully.")
        return redirect(url_for("rental_agreements.list_rental_agreements"))

@rental_agreements_bp.route("/rental_agreements/delete/<int:id>", methods = ["GET", "POST"])
def delete_rental_agreement(id):
    db_con = get_db_con()
    if request.method=="POST":
        db_con.execute("DELETE FROM rental_agreement WHERE id = ? AND user_id = ?",(id, current_user.id))
        db_con.commit()
        flash("Successfully deleted")
        return redirect(url_for("rental_agreements.list_rental_agreements"))
    
    rental_agreement = db_con.execute("SELECT * FROM rental_agreement WHERE id = ? AND user_id = ?", (id, current_user.id)).fetchone()
    return render_template("delete_rental_agreement.html", rental_agreement = rental_agreement)

@rental_agreements_bp.route("/rental_agreements/create", methods=["GET", "POST"])
def create_rental_agreement():
    conn = get_db_con()
    if request.method=="GET":
        apartments = conn.execute("""SELECT * FROM apartment WHERE id NOT IN (SELECT apartment_id FROM rental_agreement WHERE end_date IS NULL) AND user_id = ?""",(current_user.id,)).fetchall() #only the ones with active agreement - active = enddate is NULL
        tenants = conn.execute("SELECT id, name FROM tenant").fetchall()
        return render_template("create_rental_agreement.html", apartments = apartments, tenants = tenants)
    else:
        apartment_id = request.form["apartment"]
        tenant_id = request.form["tenant"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        rent_amount = request.form["rent_amount"]

        conn.execute("""
            INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, end_date, rent_amount, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (apartment_id, tenant_id, start_date, end_date, rent_amount, current_user.id))
        conn.commit()
        return redirect(url_for('rental_agreements.list_rental_agreements'))
    