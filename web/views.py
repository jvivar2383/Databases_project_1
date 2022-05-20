
from .models import Note
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json


#to define a view
#this is for the home page when we rung the website page and just add / the link will direct us to #the home page

views = Blueprint("views", __name__)

@views.route('/', methods =['GET', 'POST'])
@login_required #prevents from seeing the main page if not log in
def home():
    
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note)<2:
            flash('Note is too short!', category = 'error')
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category = 'success')
            
    #return "<h1>Welcome to our Plants Lovers Website!</h1>"
    return render_template('home.html', user = current_user)

@views.route('delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})