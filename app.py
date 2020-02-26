from flask import (Flask, render_template, request, 
                   redirect, url_for, session, flash)
from db import (add_user, login_user, add_task, get_user_id, 
                get_user_tasks, delete_task)
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'danilovdoesntliketoworkusually'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        email = request.form['email']
        username = request.form['username']
        password = request.form['pw']
        password_check = request.form['pw2']
        if password != password_check:
            return render_template('index.html', error='password_error')
        try:
            add_user(username, email, password)
        except IntegrityError:
            return render_template('index.html', error='already_exists')
        session['user'] = username
        return redirect('/users/' + username)


@app.route('/users/<name>', methods=['GET', 'POST'])
def user_page(name):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        deadline_on = request.form['deadline_on']
        user_id = get_user_id(name)
        add_task(user_id, title, content, deadline_on)
        flash(f'Task "{title}" was added!')
        return redirect('/users/' + name)
    user_id = get_user_id(name)
    tasks = get_user_tasks(user_id)
    return render_template('user.html', name=name, tasks=tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pw']
        user = login_user(email, password)
        if not user:
            return render_template('login.html', error=True)
        session['user'] = user.name
        return redirect('/users/' + user.name)
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')


@app.route('/delete/<task_id>')
def delete_tasks(task_id):
    username = session['user']
    print('username', username)
    task_to_delete = delete_task(username, task_id)
    flash(f'Task "{task_to_delete}" was removed!')
    return redirect('/users/' + username)


app.run(debug=True) # REPL: app.run('0.0.0.0', '3000', debug=True)