from locust import HttpUser, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO
import random

create_vip_package_id = []

class AdminBehaviour(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')

        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_vip_package_id:
            id = create_vip_package_id.pop()
            self.client.delete(
                f'/api/vip-packages/{id}',
                headers=headers,
                name='/cleanup'
            )
            print(len(create_vip_package_id))

    @task
    class Flow(SequentialTaskSet):
        def clear(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            while create_vip_package_id:
                id = create_vip_package_id.pop()
                self.client.delete(
                    f'/api/vip-packages/{id}',
                    headers=headers,
                    name='/cleanup'
                )

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def createVIPPackage(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            vip_package_identifier = "Locust Test VIP Package " + salt()

            response = self.client.post(
                "/api/vip-packages/",
                json={
                    "name": vip_package_identifier,
                    "description": vip_package_identifier,
                    "price": random.randint(100, 10000),
                    "durationUnit": random.choice(["DAY", "MONTH", "YEAR"]),
                    "durationNumber": random.randint(1, 30)
                },
                headers=headers
            )

            create_vip_package_id.append(response.json()['package']['_id'])

            self.clear()