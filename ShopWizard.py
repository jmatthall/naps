#!/usr/bin/env python3
'''
Purchase items from user-shops via shop wizard.

Part of naps (neopets automation program suite)
'''


from NeoSession import NeoSession


class ShopWizard(NeoSession):

    def __init__(self):
        pass

    def buy_item(self):
        url = 'http://www.neopets.com/market.phtml?type=wizard'
        resp = self.session_get(url)
        url = 'http://www.neopets.com/market.phtml'
        resp = self.session_post(url, data={
            'type': 'process_wizard', 'feedset': "0", 'shopwizard': codestone,
            'criteria': 'exact', 'min_price': "0", 'max_price': "99999"})
        link = re.search(
            r'<a href="(/browseshop.phtml?owner=[\w*]&buy_obj_info_id=[\d*]&buy_cost_neopoints=[\d*])">')
        url = 'http://neopets.com{}'.format(link.group())
        resp = self.session_get(url)
        link = re.search(
            r'<A href="(buy_item.phtml?lower=0&owner=[\w*]&obj_info_id=[\d]&g=1&xhs=\w*&old_price=26000&feat=\d*,\d*,1&_ref_ck=\w*)" onClick=')
        url = 'http://neopets.com{}'.format(link.group())
        resp = self.session_get(url)


def main():
    NeoSession()
    ShopWizard()


if __name__ == '__main__':
    main()
