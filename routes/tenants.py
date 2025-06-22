from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from db import get_db_con
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
#from logic import allowed_file, generate_secure_filename
#from forms import TenantForm, DeleteForm

tenants_bp = Blueprint ("tenants", __name__)

@tenants_bp.route("/tenants", methods = ["GET", "POST"])
def list_tenants():
    conn = get_db_con()
    if request.method=="POST":
        return redirect(url_for("tenants.create_tenant"))
    
    tenants = conn.execute('SELECT * FROM tenant WHERE user_id = ?', (current_user.id,)).fetchall()
    conn.close()
    #function to fetch all apartments and then show it in a table
    return render_template("tenants.html", tenants = tenants)


@tenants_bp.route("/tenant/edit/<int:id>", methods=["GET", "POST"])
def edit_tenant(id):
    db_con = get_db_con()
    tenant = db_con.execute("SELECT * FROM tenant WHERE id = ? AND user_id = ?", (id, current_user.id)).fetchone()

    if not tenant:
        abort(404)

    if request.method == "POST":
        name = request.form["name"]
        tel_num = request.form["tel_num"]
        db_con.execute("UPDATE tenant SET name = ?, tel_num = ? WHERE id = ? AND user_id = ?", (name, tel_num, id, current_user.id))
        db_con.commit()
        flash("Tenant updated successfully.")
        return redirect(url_for("tenants.list_tenants"))
    
    return render_template("edit_tenant.html", tenant=tenant)

@tenants_bp.route("/tenant/delete/<int:id>", methods=["GET", "POST"])
def delete_tenant(id):
    db_con = get_db_con()
    if request.method=="POST":
        db_con.execute("DELETE FROM tenant WHERE id = ? AND user_id = ?",(id,current_user.id))
        db_con.commit()
        flash("Success")
        return redirect(url_for("tenants.list_tenants"))
    
    tenant = db_con.execute("SELECT * FROM tenant WHERE id = ? AND user_id = ?", (id, current_user.id)).fetchone()
    return render_template("delete_tenant.html", tenant = tenant)

@tenants_bp.route("/tenant/create", methods=["GET", "POST"])
def create_tenant():
    if request.method=="GET":
        return render_template("create_tenant.html")
    else:
        db_con = get_db_con()
        tenant_name = request.form["name"]
        tenant_tel_num = request.form["tel_num"]
        db_con.execute("INSERT INTO tenant (tel_num,name, user_id) VALUES (?,?,?)", (tenant_tel_num, tenant_name, current_user.id))
        db_con.commit()
        return redirect(url_for("tenants.list_tenants"))