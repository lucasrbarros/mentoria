from app import create_app, db
from app.models import User
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    try:
        # Lista todos os usuários
        users = User.query.all()
        logger.info(f'Total de usuários encontrados: {len(users)}')
        
        for user in users:
            logger.info(f'ID: {user.id}')
            logger.info(f'Username: {user.username}')
            logger.info(f'Email: {user.email}')
            logger.info(f'É Senior: {user.is_senior}')
            logger.info('-' * 50)
            
    except Exception as e:
        logger.error(f'ERRO ao verificar usuários: {str(e)}')
        raise 