from flask import Blueprint, render_template, request, flash, redirect, url_for
from db.db import get_db_con
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from flask_login import current_user

rent_payments_bp = Blueprint ("rent_payments", __name__)

@rent_payments_bp.route("/rent_payments", methods = ["GET", "POST"])
def list_rent_payments():
    conn = get_db_con()# Datenbankverbindung holen
    if request.method=="POST":
        return redirect(url_for("rent_payments.create_rent_payment"))

    else:
        apartment_id = request.args.get("apartment_id")
        tenant_id = request.args.get("tenant_id")
        month = request.args.get("month")
# SQL-Abfrage, um bestehende Zahlungen abzurufen
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
            JOIN rental_agreement ra 
                ON ra.apartment_id = a.id
                AND substr(rp.month, 1, 7) BETWEEN substr(ra.start_date, 1, 7) AND IFNULL(substr(ra.end_date, 1, 7), '9999-12')            

            JOIN tenant t ON ra.tenant_id = t.id
            WHERE rp.user_id = ?                                     
        """
        params = [current_user.id]
# Optional: Filter anwenden
        if apartment_id:
            query += " AND a.id = ?"
            params.append(apartment_id)
        if tenant_id:
            query += " AND t.id = ?"
            params.append(tenant_id)
        if month:
            query += " AND rp.month = ?"
            params.append(month)
# Ergebnisse sortieren nach Zahlungsdatum (neueste zuerst)
        query += " ORDER BY rp.payment_date DESC"
        rent_payments = conn.execute(query, params).fetchall()

        # Get all apartments/tenants for the dropdowns
        apartments = conn.execute("SELECT id, name FROM apartment WHERE user_id = ?", (current_user.id,)).fetchall()
        tenants = conn.execute("SELECT id, name FROM tenant WHERE user_id = ?", (current_user.id,)).fetchall()

  # Monat formatiert darstellen („Juni 2025“)
        processed_rent_payments = []
        for payment in rent_payments:
            payment = dict(payment)
            payment["month_display"] = datetime.strptime(payment["month"], "%Y-%m").strftime("%B %Y")
            processed_rent_payments.append(payment)


        return render_template("rent_payments/rent_payments.html", rent_payments = processed_rent_payments, apartments = apartments, 
                               tenants = tenants, selected_apartment=apartment_id, 
                               selected_tenant = tenant_id, selected_month = month)


@rent_payments_bp.route("/rent_payments/create", methods=["GET", "POST"])
def create_rent_payment():
    conn = get_db_con()
    if request.method=="GET":
        # Wohnungen mit gültigem Mietvertrag anzeigen
        apartments = conn.execute("""SELECT id, name from apartment WHERE id IN (SELECT apartment_id FROM rental_agreement)
                                   AND user_id = ?""", (current_user.id,)).fetchall()
        
        today = date.today()
        next_month = (today + relativedelta(months=1)).strftime("%Y-%m")
        months = [(date.today() + relativedelta(months=i)).strftime("%Y-%m") for i in range(-6,12)]
        months_display = [ {"value": m, "label": datetime.strptime(m, "%Y-%m").strftime("%B %Y"), "selected":m==next_month} for m in months]
        return render_template("rent_payments/create_rent_payment.html", apartments = apartments, today = today, months_display = months_display)
    else:
        
        apartment_id = request.form["apartment_id"]
        selected_months = request.form.getlist("months[]")
        payment_date = request.form["payment_date"]

        skipped_months=[]
        inserted_count=0
       
        for month in selected_months:
            month_exists = conn.execute("SELECT 1 FROM rent_payment WHERE user_id = ? AND apartment_id = ? AND month = ?""", (current_user.id, apartment_id, month)).fetchone()
            if month_exists:
                skipped_months.append(month)
                continue
 # Falls nicht vorhanden → einfügen
            conn.execute("""
            INSERT INTO rent_payment (apartment_id, month, payment_date, user_id)
            VALUES (?, ?, ?, ?)
        """, (apartment_id, month, payment_date, current_user.id))
            
            inserted_count +=1

        conn.commit()

        if skipped_months:
            flash(f"⚠️ Skipped {len(skipped_months)} duplicate month(s): {', '.join(skipped_months)}", "primary")
        if inserted_count:
            flash(f"Added {inserted_count} new rent payment(s) successfully.", "add")
        if not inserted_count and not skipped_months:
            flash("ℹ️ No months selected.", "primary")

        return redirect(url_for("rent_payments.list_rent_payments"))
    
@rent_payments_bp.route("/rent_payments/edit/<int:id>", methods=["GET", "POST"])
def edit_rent_payment(id):#edit
    db_con = get_db_con()
    if request.method=="GET":
         # Bestehende Zahlung laden
        rent_payment = db_con.execute("""
            SELECT * FROM rent_payment WHERE id = ?
        """, (id,)).fetchone()

        today = date.today().isoformat()
        months = [(date.today() + relativedelta(months=i)).strftime("%Y-%m") for i in range(-6,12)]
        months_display = [ {"value": m, "label": datetime.strptime(m, "%Y-%m").strftime("%B %Y")} for m in months]
        return render_template("rent_payments/edit_rent_payment.html", rent_payment = rent_payment,today = today, months_display = months_display)
    
    else:
        month = request.form.get("month")
        apartment_id = int(request.form["apartment_id"])
# Prüfen: Gibt es bereits eine andere Zahlung für diesen Monat?
        duplicate = db_con.execute("""
        SELECT id FROM rent_payment 
        WHERE user_id = ? AND apartment_id = ? AND month = ? AND id != ?
    """, (current_user.id, apartment_id, month, id)).fetchone()

    if duplicate:
        flash("A rent payment for this apartment and month already exists.", "edit")
        return redirect(url_for("rent_payments.edit_rent_payment", id=id))

    db_con.execute("UPDATE rent_payment SET month = ? WHERE id = ? AND user_id= ?", (month, id, current_user.id))
    db_con.commit()
    flash("Rent Payment updated successfully.","edit")
    return redirect(url_for("rent_payments.list_rent_payments"))


#Delete
@rent_payments_bp.route("/rent_payments/delete/<int:id>", methods=["GET", "POST"])
def delete_rent_payment(id):
    db_con = get_db_con()
    if request.method=="POST":
        db_con.execute("DELETE FROM rent_payment WHERE id = ? AND user_id = ?",(id, current_user.id))
        db_con.commit()
        flash("Payment deleted successfully.", "delete")
        return redirect(url_for("rent_payments.list_rent_payments"))
    
    rent_payment = db_con.execute("""
    SELECT rent_payment.*,
           apartment.name AS apartment_name,
           tenant.name AS tenant_name
    FROM rent_payment
    JOIN apartment ON rent_payment.apartment_id = apartment.id
    JOIN rental_agreement
      ON rental_agreement.apartment_id = rent_payment.apartment_id
     AND substr(rental_agreement.start_date, 1, 7) <= rent_payment.month
     AND (rental_agreement.end_date IS NULL OR substr(rental_agreement.end_date, 1, 7) >= rent_payment.month)
     AND rental_agreement.user_id = rent_payment.user_id
    JOIN tenant ON rental_agreement.tenant_id = tenant.id
    WHERE rent_payment.id = ? AND rent_payment.user_id = ?
""", (id, current_user.id)).fetchone()
    return render_template("rent_payments/delete_rent_payment.html", rent_payment = rent_payment)