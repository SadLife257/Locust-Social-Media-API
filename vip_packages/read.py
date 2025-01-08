from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

class AdminBehaviour(HttpUser):
    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllVIPPackages(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/vip-packages/',
                headers=headers
            )

            self.vip_package_id = random.choice(response.json()['Packages'])['_id']

        @task
        def getVIPPackage(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/vip-packages/{self.vip_package_id}',
                headers=headers,
                name='/vip_packages'
            )