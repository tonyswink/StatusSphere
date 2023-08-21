from app import db

class Icon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value
        }
