from app import create_app, db
from app.models import User
from flask_migrate import Migrate, init, migrate, upgrade
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    try:
        # Verifica se o banco de dados existe
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mentoria.db')
        logger.info(f'Caminho do banco de dados: {db_path}')
        
        if os.path.exists(db_path):
            logger.info(f'Removendo banco de dados existente: {db_path}')
            os.remove(db_path)
        
        logger.info('Inicializando banco de dados...')
        db.create_all()
        logger.info('Banco de dados criado com sucesso!')
        
        # Cria o usuário administrador se não existir
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            logger.info('Criando usuário administrador...')
            admin = User(username='admin', email='admin@example.com', is_senior=True)
            admin.set_password('senha123')
            db.session.add(admin)
            db.session.commit()
            logger.info('Usuário administrador criado com sucesso!')
        else:
            logger.info('Usuário administrador já existe!')
            
        # Verifica se o usuário foi criado corretamente
        admin = User.query.filter_by(username='admin').first()
        if admin:
            logger.info(f'Usuário admin encontrado no banco de dados. ID: {admin.id}, Senior: {admin.is_senior}')
        else:
            logger.error('ERRO: Usuário admin não encontrado no banco de dados!')
            
        # Verifica se o arquivo do banco de dados foi criado
        if os.path.exists(db_path):
            logger.info(f'Banco de dados criado com sucesso em: {db_path}')
        else:
            logger.error(f'ERRO: Banco de dados não foi criado em: {db_path}')
            
    except Exception as e:
        logger.error(f'ERRO ao inicializar o banco de dados: {str(e)}')
        raise 