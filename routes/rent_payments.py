from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import get_db_con
from datetime import date
from dateutil.relativedelta import relativedelta

rent_payments_bp = Blueprint ("rent_payments", __name__)

@rent_payments_bp.route("/rent_payments", methods = ["GET", "POST"])
def list_rent_payments():
    conn = get_db_con()
    if request.method=="POST":
        return redirect(url_for("rent_payments.create_rent_payment"))

    rent_payments = conn.execute("""
        SELECT 
        a.name AS apartment_name,
        t.name AS tenant_name,
        ra.rent_amount,
        rp.id AS id,
        rp.month,
        rp.payment_date
        FROM rent_payment rp
        JOIN apartment a ON rp.apartment_id = a.id
        JOIN rental_agreement ra ON ra.apartment_id = a.id
        JOIN tenant t ON ra.tenant_id = t.id
        ORDER BY rp.payment_date DESC;""").fetchall()
    conn.close()
    #function to fetch all apartments and then show it in a table
    return render_template("rent_payments.html", rent_payments = rent_payments)


@rent_payments_bp.route("/rent_payments/create", methods=["GET", "POST"])
def create_rent_payment():
    conn = get_db_con()
    if request.method=="GET":
        apartments = conn.execute("""SELECT id, name from apartment WHERE id IN (SELECT apartment_id FROM rental_agreement)""").fetchall()
        today = date.today().isoformat()
        months = [(date.today() + relativedelta(months=i)).strftime("%Y-%m") for i in range(12)]
        return render_template("create_rent_payment.html", apartments = apartments, today = today, months = months)
    else:
        
        apartment_id = request.form["apartment_id"]
        selected_months = request.form.getlist("months")
        payment_date = request.form["payment_date"]

        tenant = conn.execute("""
            SELECT tenant_id FROM rental_agreement WHERE apartment_id = ?
        """, (apartment_id,)).fetchone()

        if not tenant:
            flash("No tenant is currently assigned to this apartment.", "error")
            return redirect(url_for("rent_payments.create_rent_payment"))

        tenant_id = tenant["tenant_id"]

       
        for month in selected_months:
            conn.execute("""
                INSERT INTO rent_payment (apartment_id, tenant_id, month, payment_date)
                VALUES (?, ?, ?, ?)
            """, (apartment_id, tenant_id, month, payment_date))

        conn.commit()
        flash("Rent payment(s) registered successfully.", "success")
        return redirect(url_for("rent_payments.list_rent_payments"))
    
@rent_payments_bp.route("/rent_payments/edit/<int:id>", methods=["GET", "POST"])
def edit_rent_payment(id):
    db_con = get_db_con()
    if request.method=="GET":
        # Get current agreement
        rent_payment = db_con.execute("""
            SELECT * FROM rent_payment WHERE id = ?
        """, (id,)).fetchone()

        return render_template("edit_rent_payment.html", rent_payment = rent_payment)
    
    else:
        month = request.form["month"]
        db_con.execute("UPDATE rent_payment SET month = ? WHERE id = ?", (month, id))
        db_con.commit()
        flash("Rent Payment updated successfully.")
        return redirect(url_for("rent_payments.list_rent_payments"))


@rent_payments_bp.route("/rent_payments/delete/<int:id>", methods=["GET", "POST"])
def delete_rent_payment(id):
    db_con = get_db_con()
    if request.method=="POST":
        db_con.execute("DELETE FROM rent_payment WHERE id = ?",(id,))
        db_con.commit()
        flash("Success")
        return redirect(url_for("rent_payments.list_rent_payments"))
    
    rent_payment = db_con.execute("SELECT * FROM rent_payment WHERE id = ?", (id,)).fetchone()
    return render_template("delete_rent_payment.html", rent_payment = rent_payment)