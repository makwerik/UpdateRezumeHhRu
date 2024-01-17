import time

import requests
import json


class HhRuUpdate:
    """
    Класс для поднятия резюме в поиске на hh.ru
    """

    TOKEN_FILE = 'token.json'
    AUTH_URL = 'https://hh.ru/oauth/token'
    API_URL = 'https://api.hh.ru/resumes/'

    def __init__(self, id_rezume=None, client_id=None, client_secret=None, code=None):
        """
        :param client_id: Получаем из зарегистрированного приложения
        :param client_secret: Получаем из зарегистрированного приложения
        :param code: Получаем после перехода по ссылке:
                     https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}.
                     Код будет в адресной строке
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.id_rezume = id_rezume
        self.headers = self.load_headers()

    def load_headers(self):
        """
        Загрузка заголовков с токеном из файла
        """
        try:
            with open(self.TOKEN_FILE, 'r', encoding='utf8') as file:
                access_token = json.load(file).get('access_token')
            return {'Authorization': f'Bearer {access_token}'}

        except FileNotFoundError:
            print(f"Файл {self.TOKEN_FILE} не найден. Укажите параметры: client_id, client_secret, code в конструкторе.")
        except json.JSONDecodeError:
            print(f"Ошибка декодирования файла {self.TOKEN_FILE}. Укажите корректные параметры в конструкторе.")
        return None

    def get_token(self):
        """
        Получение токена и сохранение его в файл
        :return: JSON-файл с access_token, token_type, refresh_token, expires_in
        """
        grant_type = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.code,
            'grant_type': "authorization_code",
            'redirect_uri': 'https://hh.ru/'
        }

        response = requests.post(self.AUTH_URL, data=grant_type)
        data = response.json()

        with open(self.TOKEN_FILE, 'w') as file:
            json.dump(data, file)

        print('Конфигурационный файл сохранен')
        return data

    def info_resume(self):
        """
        Получение информации по конкретному резюме
        :return: JSON с информацией по резюме
        """
        response = requests.get(f'{self.API_URL}{self.id_rezume}', headers=self.headers).json()
        return response

    def update_resume(self):
        """
        Метод поднятия резюме в поиске на hh.ru
        """
        response = requests.post(f'{self.API_URL}{self.id_rezume}/publish', headers=self.headers)

        if response.status_code == 204:
            print('Резюме поднято')
            time.sleep(14460)

        elif response.status_code == 403:
            print("Токен просрочен")
            self.refresh_token()

        elif response.status_code == 429:
            print('Объявление уже поднято')
            print(f"Следующее обновление: {self.info_resume().get('next_publish_at').split('T')}")
            time.sleep(14460)

    def refresh_token(self):
        """
        Рефреш токена и сохранение его в файл
        :return: JSON-файл с access_token, token_type, refresh_token, expires_in
        """
        with open(self.TOKEN_FILE, 'r', encoding='utf8') as file:
            refresh_token = json.load(file).get('refresh_token')

        grant_type = {
            'grant_type': "refresh_token",
            'refresh_token': f"{refresh_token}",
        }

        response = requests.post(self.AUTH_URL, data=grant_type)
        data = response.json()

        with open('token.json', 'w') as file:
            json.dump(data, file)

        print("Токен обновлен")


if __name__ == '__main__':
    hh = HhRuUpdate()
