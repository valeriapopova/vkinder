from config import token, group_token, version
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from db import engine, Session, Base, User, Match, Photos, BlackList

vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)
session = Session()
connection = engine.connect()


def search_partners(age_from, age_to, sex, city):
    partners = []
    profile_link = 'https://vk.com/id'
    result = vk.method('users.search', {
        'age_from': age_from,
        'age_to': age_to,
        'sex': sex,
        'city': city,
        'status': 6,
        'has_photo': 1
    })
    for items in result['items']:
        profile_id = f'{profile_link}{items["id"]}'
        partner = [items['first_name'], items['last_name'], profile_id]
        partners.append(partner)
    return partners


def getting_photos(owner_id):
    result = vk.method('photos.get', {
        'owner_id': owner_id,
        'album_id': 'profile',
        'access_token': token,
        'v': version,
        'extended': 1,
        'photos_sizes': 1
    })
    all_photos = []
    for res in result['items']:
        sorted_res = sorted(res, key=lambda x: x['likes']['count'], reverse=True)
        for id_photo in sorted_res:
            all_photos.append(f"photo{owner_id}_{id_photo['id']}")
        top_photos = ','.join(all_photos[:3])
        return top_photos
