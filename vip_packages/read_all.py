from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt

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

            self.client.get(
                '/api/vip-packages/',
                headers=headers
            )