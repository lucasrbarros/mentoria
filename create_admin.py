from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User(username='admin', email='admin@example.com', is_senior=True)
    user.set_password('senha123')
    db.session.add(user)
    db.session.commit()
    print('Usuário administrador criado com sucesso!') 