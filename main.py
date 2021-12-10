from random import randrange
from config import *
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk = vk_api.VkApi(token=token)
user_api = vk.get_api()



def write_msg(user_id, message, attachment=''):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
                'attachment': attachment})


vk = vk_api.VkApi(token=group_token)
api = vk.get_api()
longpoll = VkLongPoll(vk, 209285110)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "привет" or "Привет":
                write_msg(event.user_id, f"Хей, {event.user_id}, хочешь найти парнера/партнёрку?\n "
                                         f"Чтобы начать,отправь СТАРТ")
            elif request == "пока" or "Пока":
                write_msg(event.user_id, "До свидания")
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")





# if __name__ == '__main__':
