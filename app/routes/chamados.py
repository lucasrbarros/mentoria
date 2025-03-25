import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Chamado, User, FotoChamado
from app import db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('chamados', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
@login_required
def index():
    # Obtém os parâmetros de filtro da URL
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    prioridade = request.args.get('prioridade', '')
    
    logger.info(f'Filtrando chamados - Busca: {search}, Status: {status}, Prioridade: {prioridade}')
    
    # Inicia a consulta base
    query = Chamado.query
    
    # Aplica os filtros
    if search:
        query = query.filter(
            Chamado.entidade.ilike(f'%{search}%') | 
            Chamado.duvida_erro.ilike(f'%{search}%')
        )
    
    if status:
        query = query.filter(Chamado.status == status)
    
    if prioridade:
        query = query.filter(Chamado.prioridade == int(prioridade))
    
    # Ordena os resultados
    chamados = query.order_by(Chamado.created_at.desc()).all()
    
    logger.info(f'Total de chamados encontrados: {len(chamados)}')
    
    # Renderiza o template com os chamados filtrados e inclui o timedelta
    return render_template('chamados/index.html', 
                           chamados=chamados,
                           search=search, 
                           status=status, 
                           prioridade=prioridade,
                           timedelta=timedelta)

@bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        entidade = request.form['entidade']
        duvida_erro = request.form['duvida_erro']
        validacoes = request.form['validacoes']
        outros_clientes = request.form['outros_clientes']
        prioridade = request.form['prioridade']
        consultou_movidesk = 'consultou_movidesk' in request.form
        link_ambiente = request.form['link_ambiente']
        
        chamado = Chamado(
            entidade=entidade,
            duvida_erro=duvida_erro,
            validacoes=validacoes,
            outros_clientes=outros_clientes,
            consultou_movidesk=consultou_movidesk,
            link_ambiente=link_ambiente,
            prioridade=prioridade,
            autor_id=current_user.id
        )
        
        # Processa as fotos
        if 'prints' in request.files:
            files = request.files.getlist('prints')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    
                    # Cria o registro da foto
                    foto = FotoChamado(chamado=chamado, print_path=filename)
                    db.session.add(foto)
        
        db.session.add(chamado)
        db.session.commit()
        
        flash('Chamado criado com sucesso!')
        return redirect(url_for('chamados.index'))
    
    return render_template('chamados/novo.html')

@bp.route('/chamado/<int:id>')
@login_required
def visualizar(id):
    chamado = Chamado.query.get_or_404(id)
    return render_template('chamados/visualizar.html', chamado=chamado, timedelta=timedelta)

@bp.route('/chamado/<int:id>/atender')
@login_required
def atender(id):
    if not current_user.is_senior:
        flash('Apenas seniors podem atender chamados')
        return redirect(url_for('chamados.index'))
    
    chamado = Chamado.query.get_or_404(id)
    chamado.status = 'em_atendimento'
    chamado.atendente_id = current_user.id
    db.session.commit()
    
    flash('Chamado marcado como em atendimento')
    return redirect(url_for('chamados.visualizar', id=id))

@bp.route('/chamado/<int:id>/resolver')
@login_required
def resolver(id):
    if not current_user.is_senior:
        flash('Apenas seniors podem resolver chamados')
        return redirect(url_for('chamados.index'))
    
    chamado = Chamado.query.get_or_404(id)
    chamado.status = 'resolvido'
    db.session.commit()
    
    flash('Chamado marcado como resolvido')
    return redirect(url_for('chamados.index'))

@bp.route('/chamado/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    chamado = Chamado.query.get_or_404(id)
    
    # Verifica se o usuário tem permissão para excluir
    if not (current_user.is_senior or chamado.autor_id == current_user.id):
        flash('Você não tem permissão para excluir este chamado.', 'error')
        return redirect(url_for('chamados.visualizar', id=id))
    
    try:
        # Remove o arquivo de print se existir
        if chamado.print_path:
            print_path = os.path.join(current_app.config['UPLOAD_FOLDER'], chamado.print_path)
            if os.path.exists(print_path):
                os.remove(print_path)
        
        # Remove o chamado do banco de dados
        db.session.delete(chamado)
        db.session.commit()
        
        flash('Chamado excluído com sucesso!')
        return redirect(url_for('chamados.index'))
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir o chamado. Tente novamente.', 'error')
        return redirect(url_for('chamados.visualizar', id=id)) 