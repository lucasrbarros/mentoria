from app import db
from datetime import datetime

class FotoChamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chamado_id = db.Column(db.Integer, db.ForeignKey('chamado.id'), nullable=False)
    print_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidade = db.Column(db.String(100), nullable=False)
    duvida_erro = db.Column(db.Text, nullable=False)
    validacoes = db.Column(db.Text)
    outros_clientes = db.Column(db.Text)
    consultou_movidesk = db.Column(db.Boolean, default=False)
    print_path = db.Column(db.String(255))  # Mantido para compatibilidade
    link_ambiente = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pendente')  # pendente, em_atendimento, resolvido
    prioridade = db.Column(db.Integer, default=0)  # 0: normal, 1: alta, 2: urgente
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    atendente_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relacionamento com as fotos
    fotos = db.relationship('FotoChamado', backref='chamado', lazy=True, cascade='all, delete-orphan')

    def calcular_prioridade(self):
        tempo_espera = (datetime.utcnow() - self.created_at).total_seconds() / 3600  # horas
        if tempo_espera > 24:  # mais de 24 horas
            return 2  # urgente
        elif tempo_espera > 12:  # mais de 12 horas
            return 1  # alta
        return 0  # normal 