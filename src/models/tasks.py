from .conf import db

from sqlalchemy import Column, Boolean, String, Integer


class Task(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': int(self.status),
        }
