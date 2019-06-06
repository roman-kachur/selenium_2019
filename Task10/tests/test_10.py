
def test_10(litecart):
    litecart.campaign_products().add_items_to_cart().purge_cart()
    #litecart.add_items_to_cart()
    #litecart.purge_cart()
