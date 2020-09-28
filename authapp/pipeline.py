from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from io import BytesIO
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from django.core import files
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == "google-oath2":
        print(response.keys())
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.shopuserprofile.aboutMe = response['aboutMe']

        if 'picture' in response.keys():
            url = response['picture']
            resp = requests.get(url)
            if resp.status_code != requests.codes.ok:
                print('error')

            fp = BytesIO()
            fp.write(resp.content)
            file_name = url.split("/")[-1]
            user.avatar.save(file_name, files.File(fp))

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()

    elif backend.name == 'vk-oauth2':

        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.aboutMe = data['about']

        if 'photo' in response.keys():
            url = response['photo']
            resp = requests.get(url)
            print(f'{resp} | {resp.content}')
            if resp.status_code != requests.codes.ok:
                print('error')

            fp = BytesIO()
            fp.write(resp.content)
            file_name = url.split("/")[-1]
            user.avatar.save(file_name, files.File(fp))

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.save()
    return
