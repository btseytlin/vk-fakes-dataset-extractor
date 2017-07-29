#write data to sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
import datetime

#DB_LOCATION = 'vk_profiles_db.sqlite3'
_engine = None
_session = None

_base = declarative_base()

class VkProfile(_base):
    __tablename__ = 'vk_profiles'

    id = Column(Integer, autoincrement=True, primary_key=True)

    datetime_added = Column(DateTime, nullable=False)
    vk_user_id = Column(String, nullable=True, unique=True)
    profile_fake = Column(Boolean, nullable=True)
    sex = Column(Integer, nullable=True)
    city =  Column(Integer, nullable=True)
    country =  Column(Integer, nullable=True)
    has_photo =  Column(Boolean, nullable=True) 
    wall_comments =  Column(Boolean, nullable=True)
    can_see_all_posts =  Column(Boolean, nullable=True)
    can_see_audio =  Column(Boolean, nullable=True)
    can_write_private_message =  Column(Boolean, nullable=True) 
    can_send_friend_request =  Column(Boolean, nullable=True) 
    home_phone_set =  Column(Boolean, nullable=True)
    mobile_phone_set =  Column(Boolean, nullable=True)
    university_name =  Column(String, nullable=True)
    occupation_type =  Column(String, nullable=True)
    relation =  Column(Integer, nullable=True)
    site_set =  Column(Boolean, nullable=True)
    status_set =  Column(Boolean, nullable=True)
    nickname_set =  Column(Boolean, nullable=True)
    activities_set =  Column(Boolean, nullable=True)
    interests_set =  Column(Boolean, nullable=True)
    music_set =  Column(Boolean, nullable=True)
    movies_set =  Column(Boolean, nullable=True)
    tv_set =  Column(Boolean, nullable=True)
    books_set =  Column(Boolean, nullable=True)
    games_set =  Column(Boolean, nullable=True) 
    about_set =  Column(Boolean, nullable=True)
    quotes_set =  Column(Boolean, nullable=True)
    career_set =  Column(Boolean, nullable=True)
    military_set =  Column(Boolean, nullable=True)
    universities_count =  Column(Integer, nullable=True)
    schools_count =  Column(Integer, nullable=True)
    relatives_count =  Column(Integer, nullable=True)
    connections_count =  Column(Integer, nullable=True)
    albums_count =  Column(Integer, nullable=True)
    videos_count =  Column(Integer, nullable=True)
    audios_count =  Column(Integer, nullable=True)
    user_photos_count =  Column(Integer, nullable=True)
    photos_count =  Column(Integer, nullable=True)
    notes_count =  Column(Integer, nullable=True)
    friends_count =  Column(Integer, nullable=True)
    groups_count =  Column(Integer, nullable=True)
    videos_count =  Column(Integer, nullable=True)
    followers_count =  Column(Integer, nullable=True)
    pages_count =  Column(Integer, nullable=True)
    gifts_count =  Column(Integer, nullable=True)
    subscriptions_count =  Column(Integer, nullable=True)

def prepare_database(db_location):
    global _engine, _session
    _engine = create_engine('sqlite:///{}'.format(db_location), echo=False)
    _base.metadata.create_all(_engine)
    Session = sessionmaker(bind=_engine)
    _session = Session()

def add_new_profile(kwargs, db_location):
    global _session
    new_profile = VkProfile(**kwargs)

    if not _session:
        prepare_database(db_location)

    try:
        _session.add(new_profile)
        _session.commit()
    except:
        _session.rollback()
        raise

    _session.close()
    _session = None