from locust import HttpUser, between
from locustodoorpc import OdooRPCLocust
from tasks import (
    BackendReadOnlyBehavior,
    BackendWriteOnlyBehavior,
    BackendMixedBehavior,
    FrontendBehavior,
)


class BackendReadOnlyUser(OdooRPCLocust):
    wait_time = between(500, 5000)
    weight = 10

    tasks = {BackendReadOnlyBehavior}


class BackendWriteOnlyUser(OdooRPCLocust):
    wait_time = between(800, 5000)
    weight = 1

    tasks = [BackendWriteOnlyBehavior]


class BackendMixedUser(OdooRPCLocust):
    wait_time = between(500, 3000)
    weight = 5

    tasks = [BackendMixedBehavior]


class FrontendUser(HttpUser):
    wait_time = between(200, 5000)
    weight = 5

    tasks = [FrontendBehavior]
