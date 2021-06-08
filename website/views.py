from .models import User
from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_user,login_required,logout_user,current_user
from . import db
from .models import Note
import json
views=Blueprint('views',__name__)

@views.route('/notes',methods=["GET","POST"])
@login_required
def home():
    if request.method=="POST":
        note=request.form.get('note')
        if len(note)<1:
            flash("Note is too Short",category="error")
        else :
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("note added")
    return render_template("home.html",user=current_user)

@views.route('/',methods=["GET","POST"])
def about_me():
    return render_template("about_me.html",user=current_user)

@views.route('/delete-note',methods=['GET','POST'])
def delete_note():
    print("accesssed")
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
