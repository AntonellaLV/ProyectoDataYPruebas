from datetime import datetime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey


engine = create_engine('postgresql://postgres:admin@localhost/ProyectoData23')

# engine = create_engine('postgresql://<usuario>:<contrasena>@<host>/<nombre_base_de_datos>')

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'empleado'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    apellido = Column(String(50))

class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(String(50))
    fecha_hora = Column(DateTime)
    empleado_id = Column(Integer, ForeignKey('empleado.id'))
    empleado = relationship(Empleado)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True) 
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.username


Session = sessionmaker(engine)
session = Session()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)