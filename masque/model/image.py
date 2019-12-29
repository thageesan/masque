import sqlalchemy
from masque.model import Base


class Image(Base):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    file_name = sqlalchemy.Column(sqlalchemy.String(length=128))
    directory = sqlalchemy.Column(sqlalchemy.String(length=128))

    def __repr__(self):
        return "<Image(file_name='{0}', directory='{1}')>".format(self.file_name, self.directory)
