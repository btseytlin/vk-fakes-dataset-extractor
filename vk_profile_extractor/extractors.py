import vk
from urllib.parse import urlparse

class ExtractorException(Exception):
    pass

class Extractor:
    def extract(self, api, data={}):
        pass

class UserDataExtractor(Extractor):
    def extract(self, api, data={}):
        user_id = data['vk_user_id']
        vk_fields = ["sex","bdate","city","country","home_town","has_photo","domain","contacts","site","education","universities","schools","status","followers_count","occupation","nickname","relatives","relation","connections","wall_comments","activities","interests","music","movies","tv","books","games","about","quotes","can_see_all_posts","can_see_audio","can_write_private_message","can_send_friend_request","career","military", "counters"]

        user_data = api.users.get(user_ids=[user_id], fields=vk_fields)[0]

        if 'deactivated' in user_data:
            raise ExtractorException('VkProfile deactivated.')

        out_data = data.copy()

        out_data['sex'] = user_data['sex']
        out_data['city'] = user_data['city']
        out_data['country'] = user_data['country']
        out_data['has_photo'] = user_data['has_photo']
        out_data['wall_comments'] = user_data['wall_comments']
        out_data['can_see_all_posts'] = user_data['can_see_all_posts']
        out_data['can_see_audio'] = user_data['can_see_audio']
        out_data['can_write_private_message'] = user_data['can_write_private_message']
        out_data['can_send_friend_request'] = user_data['can_send_friend_request']


        out_data['home_phone_set'] = None
        if 'home_phone' in user_data:
            out_data['home_phone_set'] = 1 if user_data['home_phone'] else 0

        out_data['mobile_phone_set'] = None
        if 'mobile_phone' in user_data:
            out_data['mobile_phone_set'] = 1 if user_data['mobile_phone'] else 0

        
        out_data['university_name'] = user_data['university_name'] if 'university_name' in user_data else None
        out_data['followers_count'] = int(user_data['followers_count'])

        out_data['occupation_type'] = None
        if 'occupation' in user_data and user_data['occupation']:
            out_data['occupation_type'] = user_data['occupation']['type']

        out_data['relation'] = user_data['relation'] if 'relation' in user_data else None

        binary_fields = ['site', 'status', 'nickname', 'activities', 'interests', 'music', 'movies', 'tv', 'books', 'games', 'about', 'quotes', 'career', 'military']
        for field in binary_fields:
            out_data['{}_set'.format(field)] = None
            if field in user_data:
                out_data['{}_set'.format(field)] =  1 if user_data[field] else 0


        count_fields = ['universities', 'schools', 'relatives', 'connections']
        for field in count_fields:
            out_data['{}_count'.format(field)] = None
            if field in user_data:
                out_data['{}_count'.format(field)] = len(user_data[field])
        
        counters_fields = [
            "albums",
            "videos",
            "audios",
            "notes",
            "photos",
            "groups",
            "gifts",
            "friends",
            "user_photos",
            "followers",
            "subscriptions",
            "pages"
        ]
        for field in counters_fields:
            out_data['{}_count'.format(field)] = None
            if field in user_data['counters']:
                out_data['{}_count'.format(field)] = int(user_data['counters'][field])

        return out_data

class ExtractorChain:
    def __init__(self, extractors=None):
        self.extractors = extractors or []

    def extract_user_data(self, vk_user_id):
        session = vk.Session()
        api = vk.API(session)

        user_data = {"vk_user_id":vk_user_id}

        for extractor in self.extractors:
            user_data = extractor.extract(api, user_data)

        return user_data

def valid_vk_link(vk_link):
    if not vk_link:
        return False
    parse_result = urlparse(vk_link)
    if not parse_result.scheme and not parse_result.netloc and not 'www' in parse_result.path:
        return False #Не ссылка
    elif not 'vk.com' in parse_result.netloc and not 'vk.com' in parse_result.path:
        return False #Не ссылка ВК
    forbidden_names = ['feed', 'im', 'mail', 'friends', 'groups', 'video', 'market', 'fave', 'docs', 'apps']
    path = urlparse(vk_link).path
    if len(path) < 2 or path.count('/') > 2 or path.count('?') > 0 or path[path.find('/')+1:] in forbidden_names:
        return False #ссылка не похожа по формату на ссылку, которая указывает на профиль ВК
    return True
        
def extract_vk_user_id(vk_link):
    path = urlparse(vk_link).path
    return path[path.find('/')+1:]

def extract_vk_profile(vk_link, extractor_chain):
    if valid_vk_link(vk_link):
        vk_user_id = extract_vk_user_id(vk_link)
    else:
        #attempt to use the string provided as a vk_user_id
        if vk_link:
            vk_user_id = vk_link
        else:
            raise ExtractorException('Invalid profile link')
    try:
        return extractor_chain.extract_user_data(vk_user_id)
    except vk.exceptions.VkAPIError as e:
        if 'Invalid user id' in str(e):
            raise ExtractorException('Invalid profile link')

