from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app, send_from_directory
from db.db import get_db_con
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
from services.utils import generate_secure_filename
from forms.tenant_forms import TenantForm, DeleteForm

tenants_bp = Blueprint ("tenants", __name__)

@tenants_bp.route("/tenants", methods = ["GET", "POST"])
def list_tenants():
    conn = get_db_con()
    if request.method=="POST":
        return redirect(url_for("tenants.create_tenant")) #Create
    
     #Holt alle Mieter des aktuellen Nutzers aus der Datenbank.
    tenants = conn.execute('SELECT * FROM tenant WHERE user_id = ?', (current_user.id,)).fetchall()
    conn.close()
    #function to fetch all apartments and then show it in a table
    return render_template("tenants/tenants.html", tenants = tenants)

@tenants_bp.route("/tenant/edit/<int:id>", methods=["GET", "POST"])
def edit_tenant(id):
    db_con = get_db_con() #Daten aus der Datenbank holen
    tenant = db_con.execute("SELECT * FROM tenant WHERE id = ? AND user_id = ?", (id, current_user.id)).fetchone()

    if not tenant:
        abort(404)

    form = TenantForm(data=tenant)

    if form.validate_on_submit():
        name = form.name.data
        tel_num = form.tel_num.data
        file = form.document.data
        filename = tenant['document_filename']
#Wenn ein neues Dokument hochgeladen wurde → speichere es sicher auf dem Server.
        if file:
            filename = generate_secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        db_con.execute(
            "UPDATE tenant SET name = ?, tel_num = ?, document_filename = ? WHERE id = ? AND user_id = ?",
            (name, tel_num, filename, id, current_user.id)
        )
        db_con.commit()
        flash("Tenant updated successfully.","edit")
        return redirect(url_for("tenants.list_tenants"))

    return render_template("tenants/edit_tenant.html", form=form, tenant=tenant)


#Delete
@tenants_bp.route("/tenant/delete/<int:id>", methods=["GET", "POST"])
def delete_tenant(id):
    db_con = get_db_con()
    tenant = db_con.execute(
        "SELECT * FROM tenant WHERE id = ? AND user_id = ?", 
        (id, current_user.id)
    ).fetchone()

    if not tenant:
        abort(404)#Prüft, ob Mieter zur ID existiert. Sonst 404.

    form = DeleteForm()#Erst nach Bestätigung löschen können
    form.submit.label.text = "Delete Tenant"
    
    if form.validate_on_submit():
        db_con.execute("DELETE FROM tenant WHERE id = ? AND user_id = ?", (id, current_user.id))
        db_con.commit()
        flash("Tenant deleted successfully.","delete")
        return redirect(url_for("tenants.list_tenants"))

    return render_template("tenants/delete_tenant.html", form=form, tenant = tenant)

#Create
@tenants_bp.route("/tenant/create", methods=["GET", "POST"])
def create_tenant():
    form = TenantForm()

    if form.validate_on_submit():
        db_con = get_db_con()
        tenant_name = request.form["name"]
        tenant_tel_num = request.form["tel_num"]
        file = request.files.get("document")
        filename = None

        if file:
            filename = generate_secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
#DB Speicherung
        db_con.execute("INSERT INTO tenant (tel_num,name, user_id, document_filename) VALUES (?,?,?,?)", (tenant_tel_num, tenant_name, current_user.id, filename))
        db_con.commit()
        flash("Tenant added successfully.","add")
        return redirect(url_for("tenants.list_tenants"))
    return render_template("tenants/create_tenant.html", form=form)

@tenants_bp.route("/tenant/download/<filename>")
def download_document(filename):
    db_con = get_db_con()
    tenant = db_con.execute(
        "SELECT * FROM tenant WHERE document_filename = ? AND user_id = ?",
        (filename, current_user.id)).fetchone()
   # Prüft, ob Datei dem Benutzer gehört. Sonst Fehler.

    if not tenant:
        abort(403)
    
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

@tenants_bp.route("/tenant/view/<filename>")
def view_document(filename):
    db_con = get_db_con()
    tenant = db_con.execute(
        "SELECT * FROM tenant WHERE document_filename = ? AND user_id = ?",
        (filename, current_user.id)
    ).fetchone() #Prüft erneut Benutzerberechtigung.

    if not tenant:
        abort(403)

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=False
    )