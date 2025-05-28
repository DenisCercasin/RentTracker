from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import get_db_con
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

rent_payments_bp = Blueprint ("rent_payments", __name__)

@rent_payments_bp.route("/rent_payments", methods = ["GET", "POST"])
def list_rent_payments():
    conn = get_db_con()
    if request.method=="POST":
        return redirect(url_for("rent_payments.create_rent_payment"))

    else:
        apartment_id = request.args.get("apartment_id")
        tenant_id = request.args.get("tenant_id")
        month = request.args.get("month")

        query = """
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
            WHERE 1=1                                      --does nothing - is always true and is there 
                                                           --to safely append all other conditions
        """
        params = []

        if apartment_id:
            query += " AND a.id = ?"
            params.append(apartment_id)
        if tenant_id:
            query += " AND t.id = ?"
            params.append(tenant_id)
        if month:
            query += " AND rp.month = ?"
            params.append(month)

        query += " ORDER BY rp.payment_date DESC"
        rent_payments = conn.execute(query, params).fetchall()

        # Get all apartments/tenants for the dropdowns
        apartments = conn.execute("SELECT id, name FROM apartment").fetchall()
        tenants = conn.execute("SELECT id, name FROM tenant").fetchall()

        processed_rent_payments = []
        for payment in rent_payments:
            payment = dict(payment)
            payment["month_display"] = datetime.strptime(payment["month"], "%Y-%m").strftime("%B %Y")
            processed_rent_payments.append(payment)


        return render_template("rent_payments.html", rent_payments = processed_rent_payments, apartments = apartments, 
                               tenants = tenants, selected_apartment=apartment_id, 
                               selected_tenant = tenant_id, selected_month = month)


@rent_payments_bp.route("/rent_payments/create", methods=["GET", "POST"])
def create_rent_payment():
    conn = get_db_con()
    if request.method=="GET":
        apartments = conn.execute("""SELECT id, name from apartment WHERE id IN (SELECT apartment_id FROM rental_agreement)""").fetchall()
        today = date.today().isoformat()
        months = [(date.today() + relativedelta(months=i)).strftime("%Y-%m") for i in range(12)]
        months_display = [ {"value": m, "label": datetime.strptime(m, "%Y-%m").strftime("%B %Y")} for m in months]
        return render_template("create_rent_payment.html", apartments = apartments, today = today, months_display = months_display)
    else:
        
        apartment_id = request.form["apartment_id"]
        selected_months = request.form.getlist("months")
        payment_date = request.form["payment_date"]
       
        for month in selected_months:
            conn.execute("""
            INSERT INTO rent_payment (apartment_id, month, payment_date)
            VALUES (?, ?, ?)
        """, (apartment_id, month, payment_date))
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