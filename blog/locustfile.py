from locust import HttpLocust, TaskSet, task, between



class UserBehaviour(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post("/login", {"username":"boy", "password":"testing321"})

    def logout(self):
        self.client.post("/logout", {"username":"boy", "password":"testing321"})

@task(1)
def index(self):
    self.client.get("/")


class WebsiteUser(HttpLocust):
    host = "http://127.0.0.1:8089"
    task_set = UserBehaviour
    wait_time = between(5.0, 9.0)