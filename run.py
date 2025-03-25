from app import create_app, db
from app.models import User, Chamado
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Chamado': Chamado}

def verificar_criar_admin():
    """Verifica se existe um usuário admin ou master, caso não exista, cria um."""
    with app.app_context():
        admin = User.query.filter(User.username.in_(['admin', 'master'])).first()
        if not admin:
            logger.info("Usuário admin não encontrado. Criando usuário admin...")
            admin = User(
                username='admin',
                email='admin@example.com',
                is_senior=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            logger.info("Usuário admin criado com sucesso!")
        else:
            logger.info(f"Usuário {admin.username} já existe no sistema.")

if __name__ == '__main__':
    verificar_criar_admin()
    app.run(host='0.0.0.0')