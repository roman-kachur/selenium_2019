
def test_10(litecart):
    litecart.campaign_products()
    litecart.add_items_to_cart()
    litecart.purge_cart()
