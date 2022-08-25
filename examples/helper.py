def find_or_create_customer(client):
    Partner = client.env['res.partner']
    partner_ids = Partner.search([('customer_rank', '>', 0)], limit=1)
    if partner_ids:
        return partner_ids[0]
    else:
        return Partner.create({
            'name': 'Load testing customer',
            'customer': True,
        })


def find_or_create_sellable_product(client, index=1):
    Product = client.env['product.product']
    ref = 'LOADTEST_%d' % index
    product_ids = Product.search([('default_code', '=', ref)], limit=1)
    if product_ids:
        return product_ids[0]
    else:
        return Product.create({
            'name': 'Load testing product',
            'sale_ok': True,
            'default_code': ref,
            'type': 'product',
        })
