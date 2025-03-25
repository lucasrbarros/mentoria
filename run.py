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

if __name__ == '__main__':
app.run(debug=True, host='0.0.0.0')