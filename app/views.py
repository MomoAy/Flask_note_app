from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  login_required, current_user
from . import db
from app.models import Notes

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        return render_template("home.html", user = current_user)
    else:
        note = request.form.get("note")
        note.strip()
        if len(note)<2 : 
            flash("Note is too short", category="error")
        else : 
            new_note = Notes(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note add", category="success")
            return redirect(url_for("views.home"))

@views.route('/delete/<int:id>')
@login_required
def delete(id):
    id_sup = Notes.query.get(id)
    db.session.delete(id_sup)
    db.session.commit()
    return redirect(url_for("views.home"))