import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


# Класс перевода
class Bank(SqlAlchemyBase, SerializerMixin):
    # Название таблицы
    __tablename__ = 'banks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    from_bill = sqlalchemy.Column(sqlalchemy.Integer)   # Счёт отправителя
    to_bill = sqlalchemy.Column(sqlalchemy.Integer)  # Счёт получателя
    cost = sqlalchemy.Column(sqlalchemy.Integer)  # Сумма перевода