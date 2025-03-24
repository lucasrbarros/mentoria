from app import create_app, db
from app.models import User, Chamado

application = create_app()

if __name__ == "__main__":
    application.run() 