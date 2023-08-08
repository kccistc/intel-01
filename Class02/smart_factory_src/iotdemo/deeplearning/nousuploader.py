from queue import Queue
from threading import Thread

import cv2
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__all__ = ('NousUploader', )


class NousUploader:
    def __init__(self, base_address: str, *, async_mode: bool = True):
        self.base_url = base_address.rstrip('/')
        self.session = None
        self.token = None
        self.headers = {}

        self.force_stop = False

        if async_mode:
            self.upload = self.upload_async
            self.async_q = Queue()
            self.thread = Thread(target=self.async_task)
        else:
            self.upload = self.upload_sync
            self.async_q = None
            self.thread = None

    def async_task(self):
        q = self.async_q

        while 1:
            project_name, file_name, file_data = q.get()
            if project_name is None:
                q.task_done()
                break

            self.upload_sync(project_name, file_name, file_data)

            q.task_done()

    def login(self, nous_id: str, nous_pw: str):
        session = requests.Session()

        # fetch token
        res = session.post(f'{self.base_url}/authentication',
                           data={
                               "username": f"{nous_id}",
                               "password": f"{nous_pw}"
                           },
                           files={'_': '_'},
                           verify=False)

        # store token
        self.token = res.json().get('secure_token', '')
        self.session = session
        self.headers["Authorization"] = f"bearer_token {self.token}"

        # fetch project ids
        res = session.get(f'{self.base_url}/projects',
                          headers=self.headers,
                          verify=False)

        projects = res.json().get('items', [])
        self.project_ids = {data['name']: data['id'] for data in projects}

        if self.thread:
            self.thread.start()

    def upload_async(self, project_name: str, file_name: str, file_data):
        if self.force_stop:
            return

        file_data = file_data.copy()
        self.async_q.put_nowait((project_name, file_name, file_data))

    def upload_sync(self, project_name: str, file_name: str, file_data):
        project_id = self.project_ids[project_name]
        file_data = cv2.imencode(".jpg", file_data)[1]

        res = self.session.post(
            f'{self.base_url}/projects/{project_id}/media/images',
            headers=self.headers,
            files={
                'file': (file_name, file_data.tobytes(), 'image/jpeg', {
                    'Expires': '0'
                })
            },
            verify=False)

        return res.status_code == 200

    def close(self):
        if self.async_q:
            self.async_q.put_nowait((None, None, None))
            self.async_q.join()
            self.thread.join()

        self.force_stop = True
        self.session.close()
