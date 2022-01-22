from dataclasses import dataclass
from sqlalchemy import Column, String
from sqlalchemy import exc
from .db import Base, session

@dataclass
class Users(Base):
    __tablename__ = 'users'
    name: str
    mal_username: str

    name = Column(String, nullable=False)
    mal_username = Column(String, primary_key=True)


    def add_user(username: str, user_id: str):
        if None in (username, user_id):
            print('username or user_id is None')
            raise ValueError
        try:
            user = Users(name=username, mal_username=user_id)
            session.add(user)
            session.commit()
            print(f'Added {user.name} to database')
            return
        except exc.SQLAlchemyError as e:
            raise e


    def get_users():
        users = session.query(Users).all()
        print (users)
        return users


    def delete_user(user_id: str):
        if user_id is None:
            print('user_id is None')
            raise ValueError
        try:
            user = session.query(Users).filter_by(mal_username=user_id).first()
            session.delete(user)
            session.commit()
            print(f'Deleted {user.name} from database')
            return
        except exc.SQLAlchemyError as e:
            raise e
