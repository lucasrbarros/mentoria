from app import create_app, db
from app.models import User
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Lista de usuários técnicos
tecnicos = [
    {'username': 'lucas.barros', 'email': 'lucas.barros@example.com', 'is_senior': False},
    {'username': 'sabrina.leite', 'email': 'sabrina.leite@example.com', 'is_senior': False},
    {'username': 'pedro.fonseca', 'email': 'pedro.fonseca@example.com', 'is_senior': False},
    {'username': 'rodrigo.pozza', 'email': 'rodrigo.pozza@example.com', 'is_senior': False},
    {'username': 'victor.espindola', 'email': 'victor.espindola@example.com', 'is_senior': False},
    {'username': 'joao.wiezel', 'email': 'joao.wiezel@example.com', 'is_senior': False},
]

# Lista de usuários seniors
seniors = [
    {'username': 'larissa.benedetti', 'email': 'larissa.benedetti@example.com', 'is_senior': True},
]

app = create_app()

with app.app_context():
    try:
        # Cria usuários técnicos
        for tecnico in tecnicos:
            user = User.query.filter_by(username=tecnico['username']).first()
            if not user:
                logger.info(f'Criando usuário técnico: {tecnico["username"]}')
                user = User(
                    username=tecnico['username'],
                    email=tecnico['email'],
                    is_senior=tecnico['is_senior']
                )
                user.set_password('senha123')  # Senha padrão para todos os usuários
                db.session.add(user)
                logger.info(f'Usuário técnico {tecnico["username"]} criado com sucesso!')
            else:
                logger.info(f'Usuário técnico {tecnico["username"]} já existe!')

        # Cria usuários seniors
        for senior in seniors:
            user = User.query.filter_by(username=senior['username']).first()
            if not user:
                logger.info(f'Criando usuário senior: {senior["username"]}')
                user = User(
                    username=senior['username'],
                    email=senior['email'],
                    is_senior=senior['is_senior']
                )
                user.set_password('senha123')  # Senha padrão para todos os usuários
                db.session.add(user)
                logger.info(f'Usuário senior {senior["username"]} criado com sucesso!')
            else:
                logger.info(f'Usuário senior {senior["username"]} já existe!')

        # Commit das alterações
        db.session.commit()
        logger.info('Todos os usuários foram criados com sucesso!')

        # Lista todos os usuários criados
        logger.info('\nLista de usuários criados:')
        for user in User.query.all():
            logger.info(f'Username: {user.username}, Email: {user.email}, Senior: {user.is_senior}')

    except Exception as e:
        logger.error(f'ERRO ao criar usuários: {str(e)}')
        raise 