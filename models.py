from db import db

class Guest(db.Model):
    __tablename__ = "guest"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Guest {self.email}>"
