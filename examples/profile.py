from locust import HttpLocust
from locustodoorpc import OdooRPCLocust
from tasks import (
    BackendReadOnlyBehavior,
    BackendWriteOnlyBehavior,
    BackendMixedBehavior,
    FrontendBehavior,
)


class BackendReadOnlyUser(OdooRPCLocust):
    min_wait = 500
    max_wait = 5000
    weight = 10

    task_set = BackendReadOnlyBehavior


class BackendWriteOnlyUser(OdooRPCLocust):
    min_wait = 800
    max_wait = 5000
    weight = 1

    task_set = BackendWriteOnlyBehavior


class BackendMixedUser(OdooRPCLocust):
    min_wait = 500
    max_wait = 3000
    weight = 5

    task_set = BackendMixedBehavior


class FrontendUser(HttpLocust):
    min_wait = 200
    max_wait = 5000
    weight = 5

    task_set = FrontendBehavior
