import threading
import time
from flask import Flask, render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db, storage_df
from app.algo import bring_box_fn, send_box_back_fn
from app.forms import LoginForm, SearchForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Job, StorageList, User
from datetime import datetime
from app import jobs, robots_list, lift_list

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',  title = 'Home')#, user = user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('startseite'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = url_for('startseite')
        next_page = request.args.get('next') #Not required for now
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('startseite')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/startseite', methods=['GET', 'POST'])
@login_required
def startseite():
    # return render_template('storage_list.html', storage_df = storage_df.values.tolist())
    return redirect(url_for('storage_list'))

@app.route('/storage_list', methods=['GET', 'POST'])
@login_required
def storage_list():
    d = {}
    for row in StorageList.query.all():
        if row.box_num not in d:
            d[row.box_num] = []
        d[row.box_num].append(row.content)
    
    search = SearchForm(request.form)
    if request.method == 'POST': #do on button basis
        if request.form['submit_button'] == 'Search':
            results = {}
            search_string = search.data['search'].lower()
            for k in d:
                temp = ' '.join(d[k]).lower()
                if search_string in temp:
                    results[k] = d[k]
            return render_template('storage_list.html', storage_df = results, form=search)
    return render_template('storage_list.html', storage_df = d, form=search)

@app.route('/storage_list_editable', methods=['GET', 'POST'])
@login_required
def storage_list_editable():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Box bringen':
            key = request.form['key']
            content = request.form['content']
            bring_box(key)
            # bring the box with number key and content content
            storage_df = [(ele.box_num, ele.content) for ele in StorageList.query.filter_by(box_num=key).all()]
            flash("Der Roboter kommt, nehmen Sie bitte die Änderungen vor und drücken Sie 'Speichern', sobald Sie Dinge in die Box gelegt/herausgenommen haben.")
            return render_template('storage_list_editable.html', storage_df = storage_df)
    return redirect(url_for('startseite'))

def bring_box(box_number):
    # bring the box with number box_number
    job = Job(time.time(), box_number)
    jobs[0] = job
    thread = threading.Thread(target=bring_box_fn, args=(jobs, robots_list, lift_list))
    thread.start()


@app.route('/save_edited_content', methods=['GET', 'POST'])
@login_required
def save_edited_content():
    if request.method == 'POST':
        if request.form['submit_button'] == 'save':
            thread = threading.Thread(target=send_box_back_fn, args=(jobs, robots_list, lift_list))
            thread.start()
            data = []
            data_length = request.form.get('data_length')
            for i in range(int(data_length)):
                cur_key = request.form.get(f"key_{i}")
                if not cur_key:
                    continue
                cur_content = request.form.get(f"content_{i}")
                if not cur_content:
                    continue
                
                data.append((cur_key, cur_content))
            StorageList.query.filter_by(box_num=int(data[0][0])).delete()
            db.session.commit()
            for ele in data:
                obj = StorageList(box_num=int(ele[0]), content=ele[1])
                db.session.add(obj)

            db.session.commit()
            flash('Content saved scuccessfully!')
    
    return redirect(url_for('startseite'))