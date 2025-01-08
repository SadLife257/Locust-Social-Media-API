from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

create_vip_package = []

class AdminBehaviour(HttpUser):
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

        create_vip_package.append(response.json()['package'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(5):
            self.createVIPPackage()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_vip_package:
            id = create_vip_package.pop()['_id']
            self.client.delete(
                f'/api/vip-packages/{id}',
                headers=headers,
                name='/cleanup'
            )
            print(len(create_vip_package))

    @task
    class Flow(SequentialTaskSet):
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

            create_vip_package.append(response.json()['package'])

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

            removed_vip_package = random.choice(create_vip_package)
            self.vip_package_id = removed_vip_package['_id']
            create_vip_package.remove(removed_vip_package)

        @task
        def deleteVIPPackageWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/vip-packages/{self.vip_package_id}',
                name='/deleted_vip_packages',
                headers=headers
            )

            self.createVIPPackage()