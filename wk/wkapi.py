from argparse import ArgumentError
from datetime import datetime
import math
import requests
import time
from wk.structures import *

BASE_API_URL = 'https://api.wanikani.com/v2'

class WkAPI:
    def __init__(self, token: str) -> None:
        self.auth_header = {'Authorization': f'Bearer {token}'}

    def _get(self, url: str) -> dict:
        try:
            res = requests.get(url, headers=self.auth_header)
            json_res = res.json()

            if 'error' in json_res and 'code' in json_res:
                print(f'dbg: Error response {json_res["code"]} ({json_res["error"]})')
                if json_res['code'] == 429: # Rate Limit
                    wait = int(res.headers['RateLimit-Reset']) - math.ceil(datetime.now().timestamp())
                    print(f'dbg: We are being rate limited. Retry in {wait} seconds')
                    time.sleep(wait)
                    print('dbg: Retrying now...')
                    return self._get(url)

            return json_res
        except Exception as e:
            print(f'err: Exception while performing GET: {str(e)}')
            return dict()

    def get_all_assignments(self, **kwargs) -> list[Assignment]:
        arr = []
        next_url = f'{BASE_API_URL}/assignments'
        while (res := requests.get(next_url, headers=self.auth_header).json())['data'] is not None:
            for e in res['data']:
                arr.append(Assignment(e))

            if (next_url := res['pages']['next_url']) is None:
                break

        return arr

    def get_assignment(self, id: int) -> Assignment:
        return Assignment(requests.get(f'{BASE_API_URL}/assignments/{id}', headers=self.auth_header).json())


    def get_all_level_progressions(self, **kwargs) -> list[LevelProgression]:
        arr = []
        next_url = f'{BASE_API_URL}/level_progressions'
        while (res := requests.get(next_url, headers=self.auth_header).json())['data'] is not None:
            for e in res['data']:
                arr.append(LevelProgression(e))

            if (next_url := res['pages']['next_url']) is None:
                break

        return arr

    def get_level_progression(self, id: int) -> LevelProgression:
        return LevelProgression(requests.get(f'{BASE_API_URL}/level_progressions/{id}', headers=self.auth_header).json())

    def get_all_reviews(self, **kwargs) -> list[Review]:
        arr = []
        next_url = f'{BASE_API_URL}/reviews'
        while (res := self._get(next_url))['data'] is not None:
            for e in res['data']:
                arr.append(Review(e))

            if (next_url := res['pages']['next_url']) is None:
                break

        return arr

    def get_review(self, id: int) -> Review:
        return Review(requests.get(f'{BASE_API_URL}/reviews/{id}', headers=self.auth_header).json())

    def get_all_subjects(self, **kwargs) -> list[Subject]:
        arr = []
        next_url = f'{BASE_API_URL}/subjects'
        while (res := requests.get(next_url, headers=self.auth_header).json())['data'] is not None:
            for e in res['data']:
                arr.append(self._new_subject(e))

            if (next_url := res['pages']['next_url']) is None:
                break

        return arr

    def get_subject(self, id: int) -> Subject:
        return self._new_subject(requests.get(f'{BASE_API_URL}/subjects/{id}', headers=self.auth_header).json())

    def _new_subject(self, data: dict) -> Subject:
        if data['object'] == 'radical':
            return Radical(data)
        elif data['object'] == 'kanji':
            return Kanji(data)
        elif data['object'] == 'vocabulary':
            return Vocabulary(data)
        else:
            raise ArgumentError('Invalid data')
