import time

import requests
import vk_api
from python3_anticaptcha import ImageToTextTask


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """
    """ Для решении капчи используется сервис https://anti-captcha.com/
        от вас требуется только ввести token пользователя
        1000 рекапч = ~70 рублей
    """
    token = ''
    key = ImageToTextTask.ImageToTextTask(anticaptcha_key=token,
                                          save_format='const').captcha_handler(captcha_link=captcha.get_url())
    print(captcha.get_url())
    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key['solution']['text'])


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция."""
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True
    return key, remember_device


counter = 1000  # Сколько требуется отправить комментариев
delay = 2  # Задержка между сообщения(измеряется в секундах: 1=1 секунда)
login, password = 'логин', 'пароль'
owner_id = 14524722  # id сообщества Вконтакте
post_id = 1166777  # id поста сообщества
message = '#марусявключирок'  # Сообщение которое пранируется написать в комментарии

session = requests.Session()
vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler,
                          captcha_handler=captcha_handler)  # вход в аккаунт VK
try:
    vk_session.auth()  # авторизация
    i = 0
    while i <= counter:
        vk_session.method('wall.createComment',
                          {'owner_id': -owner_id, 'post_id': post_id, 'message': message})
        time.sleep(2)
        i += 1
        print(i)
except vk_api.AuthError as error_msg:
    print(error_msg)