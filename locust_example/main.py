from locust import HttpUser, between, task


class RestApiTest(HttpUser):
    wait_time = between(5, 10)

    @task
    def task_sample(self):
        self.client.get("/users")
