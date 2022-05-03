from locust import HttpUser, TaskSet, between, constant, task


class UserBehavior(TaskSet):
    @task(1)
    def profile(self):
        self.client.get("/", verify=False)


class WebsiteUser(HttpUser):
    tasks = {UserBehavior: 1}
    wait_time = constant(0)
