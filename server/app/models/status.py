from app import db

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    icon = db.Column(db.String, nullable=False)
    message = db.Column(db.String(200), nullable=False)
    animation = db.Column(db.Boolean, nullable=False)
    is_preset = db.Column(db.Boolean, default=False, nullable=False)
    is_current = db.Column(db.Boolean, default=False, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'color': self.color,
            'icon': self.icon,
            'message': self.message,
            'animation': self.animation,
            'is_preset': self.is_preset,
            'is_current': self.is_current
        }
