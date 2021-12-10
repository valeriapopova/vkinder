import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import *

Base = declarative_base()
engine = sq.create_engine(f'postgresql+psycops2://{username}:{password}@localhost:{port}/{db_name}')
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    id_vk = sq.Column(sq.Integer)


class Match(Base):
    __tablename__ = 'match'
    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    link = sq.Column(sq.String)
    city = sq.Column(sq.String)
    id_vk = sq.Column(sq.Integer, unique=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


class Photos(Base):
    __tablename__ = 'photos'
    id = sq.Column(sq.Integer, primary_key=True)
    photo_link = sq.Column(sq.String)
    likes_count = sq.String(sq.Integer)
    id_match = sq.Column(sq.Integer, sq.ForeignKey('match.id', ondelete='CASCADE'))


class BlackList(Base):
    __tablename__ = 'black_list'
    id = sq.Column(sq.Integer, primary_key=True)
    id_vk = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    link = sq.Column(sq.String)
    photo_link = sq.Column(sq.String)
    city = sq.Column(sq.String)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


def create_tables():
    Base.metadata.create_all(engine)


def add_user(id_vk):
    session.expire_on_commit = False
    add_new_user = User(id_vk=id_vk)
    session.add(add_new_user)
    session.commit()
    return True


def add_match(first_name, last_name, city, link , id_user, id_vk):
    session.expire_on_commit = False
    add_new_match = Match(id_vk=id_vk, first_name=first_name, lats_name=last_name, city=city, link=link, id_user=id_user)
    session.add(add_new_match)
    session.commit()
    return True


def add_photo(photo_link, likes_count, id_match):
    session.expire_on_commit = False
    photo = Photos(photo_link=photo_link, likes_count=likes_count, id_match=id_match)
    session.add(photo)
    session.commit()
    return True


def add_to_black_list(id_vk, first_name , last_name, link, photo_link, city, user_id):
    add_bl = BlackList(id_vk=id_vk, first_name=first_name, last_name=last_name, link=link,
                       photo_link=photo_link, city=city, user_id=user_id)
    session.add(add_bl)
    session.commit()
    return True


def user_registration(id_vk):
    new_user = User(id_vk=id_vk)
    session.add(new_user)
    session.commit()
    return True


def delete_match(vk_id):
    user_match = session.query(Match).filter_by(id_vk=vk_id).first()
    session.delete(user_match)
    session.commit()


def delete_from_bl(vk_id):
    user_bl = session.query(BlackList).filter_by(id_vk=vk_id).first()
    session.delete(user_bl)
    session.commit()

