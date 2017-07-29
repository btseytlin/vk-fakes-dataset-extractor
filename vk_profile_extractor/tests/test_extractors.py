import vk
import json
import pytest

from ..extractors import ExtractorChain, UserDataExtractor, extract_vk_profile, ExtractorException

@pytest.fixture(scope='module')
def vk_api():
    service_key = '31735d2131735d2131735d21ed312e2ad13317331735d21680479f80bb70a7b7d66fca7'
    session = vk.Session(access_token=service_key)
    api = vk.API(session, v='5.67')
    return api

@pytest.fixture(scope='module')
def extractor_chain():
    extractor_chain = ExtractorChain()
    extractor = UserDataExtractor()
    extractor_chain.extractors.append(extractor)
    return extractor_chain

@pytest.fixture(scope='module', params=['https://vk.com/btseytlin','www.vk.com/btseytlin', 'btseytlin','id43447713', '43447713' ]) #params have to be valid links pointing at same profile, but of different formats, and valid vk ids
def vk_valid_profile_id(request):
    return request.param

@pytest.fixture(scope='module', params=['https://vk.com/im','www.vk.com/btseytlinzsadasd', 'vk.com/btseytlin', '///', 'https://yandex.com/btseytlin','https://vk.ru/btseytlin', '']) #invalid vk profile links
def vk_invalid_profile_link(request):
    return request.param

@pytest.fixture(scope='module', params=['https://vk.com/id157666829']) #deleted vk profile links
def vk_valid_deleted_profile_link(request):
    return request.param



class TestVKProfileParsing(object):
    def test_valid_real_profile(self, vk_api, extractor_chain, vk_valid_profile_id):
        data = extract_vk_profile(vk_valid_profile_id, extractor_chain)
        actual_data = {
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
            'followers_count': 319,
            'pages_count': None,
            'gifts_count': None,
            'subscriptions_count': None,
        }

        for key in actual_data:
            assert key in data
            assert actual_data[key] == data[key]

    def test_invalid_profile(self, vk_api, extractor_chain, vk_invalid_profile_link):
        with pytest.raises(ExtractorException):
            data = extract_vk_profile(vk_invalid_profile_link, extractor_chain)

    def test_valid_deleted_profile(self, vk_api, extractor_chain, vk_valid_deleted_profile_link):
        with pytest.raises(ExtractorException):
            data = extract_vk_profile(vk_valid_deleted_profile_link, extractor_chain)


