from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chamados.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        logger.info(f'Tentativa de login - Username: {username}')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            logger.error(f'Usuário não encontrado: {username}')
            flash('Usuário ou senha inválidos')
            return redirect(url_for('auth.login'))
        
        if not user.check_password(password):
            logger.error(f'Senha incorreta para o usuário: {username}')
            flash('Usuário ou senha inválidos')
            return redirect(url_for('auth.login'))
        
        logger.info(f'Login bem-sucedido para o usuário: {username}')
        login_user(user)
        
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('chamados.index')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chamados.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_senior = 'is_senior' in request.form
        
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email, is_senior=is_senior)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        logger.info(f'Usuário {username} criado com sucesso. Senior: {is_senior}')
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html') 