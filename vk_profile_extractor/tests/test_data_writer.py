import pytest
import datetime
from ..data_writer import add_new_profile, VkProfile

import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

import sqlite3
@pytest.fixture(scope='module')
def db_location():
    return 'test_vk_profiles_db.sqlite3'

profile_data = {
            'datetime_added': datetime.datetime.now(),
            'vk_user_id': 'btseytlin',
            'profile_fake': False,
            'sex': 2,
            'city': 1,
            'country': 1,
            'has_photo': 1, 
            'wall_comments': 1,
            'can_see_all_posts': 0,
            'can_see_audio': 0,
            'can_write_private_message': 1, 
            'can_send_friend_request': 1, 
            'home_phone_set': 0,
            'mobile_phone_set': None,
            'university_name': None,
            'followers_count': 321,
            'occupation_type': "university",
            'relation': None,
            'site_set': 0,
            'status_set': 1,
            'nickname_set': 0,
            'activities_set': None,
            'interests_set': None,
            'music_set': None,
            'movies_set': None,
            'tv_set': None,
            'books_set': None,
            'games_set': None, 
            'about_set': None,
            'quotes_set': None,
            'career_set': None,
            'military_set': None,
            'universities_count': None,
            'schools_count': None,
            'relatives_count': None,
            'connections_count': None,
            'albums_count': 1,
            'videos_count': 55, 
            'audios_count': 0,
            'photos_count': 226,
            'user_photos_count': None,
            'notes_count': 3,
            'friends_count': None,
            'groups_count': None,
            'videos_count': 55,
            'followers_count': 321,
            'pages_count': None,
            'gifts_count': None,
            'subscriptions_count': None,
        }

class TestProfileWriting(object):
    def test_add_valid_profile(self, db_location):
        if os.path.isfile(db_location):
            os.remove(db_location)

        add_new_profile(profile_data, db_location)

        #check that added object exists in database
        engine = create_engine('sqlite:///{}'.format(db_location), echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_result = session.query(VkProfile.vk_user_id == profile_data['vk_user_id'])
        assert query_result and query_result[0]
        
        session.close()
        if os.path.isfile(db_location):
            os.remove(db_location)

    def test_add_duplicate_row(self, db_location):
        if os.path.isfile(db_location):
            os.remove(db_location)

        add_new_profile(profile_data, db_location)

        #check that added object exists in database
        engine = create_engine('sqlite:///{}'.format(db_location), echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_result = session.query(VkProfile.vk_user_id == profile_data['vk_user_id'])
        assert query_result and query_result[0]
        
        #try to add a new identical profile
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            add_new_profile(profile_data, db_location)

        #after the exception has been suppressed, add a new profile
        new_profile_data = profile_data.copy()
        new_profile_data['vk_user_id'] = 'fubar'

        add_new_profile(new_profile_data, db_location)

        query_result = session.query(VkProfile.vk_user_id == new_profile_data['vk_user_id'])
        assert query_result and query_result[0]

        session.close()
        if os.path.isfile(db_location):
            os.remove(db_location)