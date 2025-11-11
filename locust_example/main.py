from locust import HttpUser, between, task


class RestApiTest(HttpUser):
    wait_time = between(2, 5)

    @task
    def task_sample(self):
        self.client.get("/users")
