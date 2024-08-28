import aiohttp
import asyncio
from typing import Dict, Union, List
from loguru import logger
from .pydantic_models import JsonResponse
from .config import YDX_OAUTH



class ApiClient:
    def __init__(self):
        self.OAUTH = YDX_OAUTH
        self.base_url = 'https://cloud-api.yandex.net/v1'

    def _read_data(self, data: dict) -> Union[List, None]:
        list_of_files = []
        try:
            response = JsonResponse(**data)
        except Exception as e:
            logger.error(f"Ошибка распаковки: {e}")
            return None

        # Получение списка name и file из элементов items
        try:
            for item in response.embedded.items:
                list_of_files.append({'filename': item.name, 'download_url': item.file})
            return list_of_files
        except Exception as e:
            logger.error(f"Ошибка получения по ключам: {e}")
            return None

    async def _fetch_yandex_disk_public_resources(self, public_key: str) -> Union[Dict, None]:
        url = self.base_url + '/disk/public/resources'

        params = {
            'public_key': public_key,
        }
        headers = {
            'Authorization': self.OAUTH
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Ошибка: {response.status}, {response.reason}")
                    return None

    def main(self, public_key) -> Union[Dict, None]:
        data = asyncio.run(self._fetch_yandex_disk_public_resources(public_key=public_key))
        process_data = self._read_data(data)
        return process_data






