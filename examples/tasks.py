import random

from locust import task, TaskSet

import helper


class BaseBrowsingBehavior(TaskSet):

    @task(100)
    def read_partners(self, limit=80):
        Partner = self.client.env['res.partner']
        partner_ids = Partner.search([], limit=limit)
        Partner.read(partner_ids)

    @task(20)
    def read_products(self, limit=80):
        Product = self.client.env['product.product']
        product_ids = Product.search([], limit=limit)
        Product.read(product_ids)

    @task(1)
    def stop(self):
        self.interrupt()


class BaseSalesBehavior(TaskSet):

    def __init__(self, *args, **kwargs):
        super(BaseSalesBehavior, self).__init__(*args, **kwargs)
        self.Sale = self.client.env['sale.order']

    def _create_sale(self, number_of_lines=None):
        if not number_of_lines:
            number_of_lines = random.randint(1, 15)

        partner_id = helper.find_or_create_customer(self.client)
        lines = []
        for idx in range(1, number_of_lines + 1):
            product_id = helper.find_or_create_sellable_product(
                self.client, idx
            )
            line_values = {'product_id': product_id,
                           'product_uom_qty': random.randint(1, 100)}
            line = (0, 0, line_values)
            lines.append(line)
        order_id = self.Sale.create(
            {'partner_id': partner_id,
             'order_line': lines,
             }
        )
        return order_id

    def _confirm_sale(self, order_id):
        self.Sale.action_confirm([order_id])

    @task(20)
    def new_sale(self):
        order_id = self._create_sale()
        self._confirm_sale(order_id)

    @task(5)
    def stop(self):
        self.interrupt()


class BaseBackendBehavior(TaskSet):

    def on_start(self):
        self.client.login(self.locust.db_name,
                          self.locust.login,
                          self.locust.password)


class BackendReadOnlyBehavior(BaseBackendBehavior):
    tasks = {BaseBrowsingBehavior: 1}


class BackendWriteOnlyBehavior(BaseBackendBehavior):
    tasks = {BaseSalesBehavior: 1}


class BackendMixedBehavior(BaseBackendBehavior):
    tasks = {BaseBrowsingBehavior: 5, BaseSalesBehavior: 1}


class FrontendBehavior(TaskSet):

    @task(10)
    def index(self):
        self.client.get("/")

    @task(4)
    def shop(self):
        self.client.get("/shop")

    @task(5)
    def contactus(self):
        self.client.get("/page/contactus")
