import json
from functools import partialmethod
from typing import Union, Dict, List, Any
import requests

JSONType = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]


class RestError(Exception):
    """
    Error from REST API Client.
    """


def authenticate_user(username, password):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {'username': username, 'password': password}

    response = requests.post('http://localhost:8009/users/api/token/', headers=headers, data=json.dumps(data))
    return response


class RestClient:
    def __init__(self, base_url: str, **session_kwargs):
        self.base_url = base_url
        self._session = requests.Session()

        for key, value in session_kwargs.items():
            setattr(self._session, key, value)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        return self._session.close()

    def request(self, method: str, path: str, **kwargs) -> JSONType:
        try:
            resp = self._session.request(method, f'{self.base_url}/{path}', headers=self._session.headers,
                                         data=json.dumps(kwargs))
            return resp.json()
        except requests.HTTPError as http_error:
            raise RestError(f'Invalid request from {self.base_url}: {http_error}') from http_error
        except requests.RequestException as err:
            raise RestError(err) from err

    get = partialmethod(request, 'GET')
    post = partialmethod(request, 'POST')
    put = partialmethod(request, 'PUT')
    patch = partialmethod(request, 'PATCH')
    delete = partialmethod(request, 'DELETE')
    head = partialmethod(request, 'HEAD')
    options = partialmethod(request, 'OPTIONS')


DEFAULT_HEADERS = {'accept': 'application/json', 'Content-Type': 'application/json',
                   'User-Agent': 'python-requests'}


class SocialNetworkError(Exception):
    """
    Error from Social Network REST API.
    """


class SocialNetworkClient(RestClient):
    BASE_URL = 'http://localhost:8009'

    def __init__(self, username: str = None, token: str = None, headers: Dict[str, str] = None):
        headers = DEFAULT_HEADERS
        if None not in [username, token]:
            auth = authenticate_user(username, token)
            auth_token = 'JWT ' + str(auth.json()['token']['access'])
            headers = {'accept': 'application/json', 'Content-Type': 'application/json',
                       'User-Agent': 'python-requests',
                       'Authorization': auth_token}

        super().__init__(self.BASE_URL, headers=headers)

    def __enter__(self):
        return self

    @property
    def username(self) -> str:
        return self._session.auth.username

    @username.setter
    def username(self, username: str):
        self._session.auth.username = username

    @property
    def token(self) -> str:
        return self._session.auth.password

    @token.setter
    def token(self, token: str):
        self._session.auth.password = token

    def register_dumy_users(self, register_data) -> List[Dict[str, Any]]:
        return self.post(f'users/api/register/', **register_data)

    def get_posts_list(self) -> List[Dict[str, Any]]:
        return self.get('users/api/post/')

    def get_user_posts(self, user) -> List[Dict[str, Any]]:
        return self.get(f'users/api/post/{user}')

    def get_user(self, user: str) -> Dict[str, Any]:
        return self.get(f'users/{user}')

    def create_dumy_post(self, post_data) -> List[Dict[str, Any]]:
        return self.post(f'users/api/post/', **post_data)

    def like_post(self, liked_by) -> List[Dict[str, Any]]:
        return self.post(f'users/api/like_post/', **liked_by)

    def unlike_post(self, liked_by) -> List[Dict[str, Any]]:
        return self.delete(f'users/api/unlike_post/', **liked_by)
