from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill all fields', 'error')
            return redirect(url_for('auth.login'))
        
        user_model = UserModel()
        user = user_model.get_user_by_username(username)
        user_model.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('routes.index'))
        
        flash('Invalid username or password', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not password or not confirm_password:
            flash('Please fill all fields', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))
        
        user_model = UserModel()
        try:
            hashed_password = generate_password_hash(password)
            user_model.insert_user(username, hashed_password)
            user_model.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            user_model.close()
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login')) 