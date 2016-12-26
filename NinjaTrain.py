#!/usr/bin/env python3
'''Auto trainer for the ninja training school.'''

import schedule
import re
import time
import random
from NeoSession import NeoSession


class NinjaTrain(NeoSession):
    pet = NeoSession.conf['USER-SETTINGS']['PET-NAME']

    def __init__(self):
        self.course_type = self.determine_course()
        self.check_status_run()
        #self.check_buy_codestone()

    def check_buy_codestone(self):
        url = 'http://www.neopets.com/island/fight_training.phtml?type=status'
        resp = self.session_get(url)
        codestone = re.search(r'(.+ codestone)', resp.text)
        url = 'http://www.neopets.com/inventory.phtml'
        resp = self.session_get(url)
        if codestone.group() not in resp.text:
            url = 'http://www.neopets.com/market.phtml?type=wizard'
            resp = self.session_get(url)
            url = 'http://www.neopets.com/market.phtml'
            resp = self.session_post(url, data={
                'type': 'process_wizard', 'feedset': "0", 'shopwizard': codestone,
                'criteria': 'exact', 'min_price': "0", 'max_price': "99999"})
            link = re.search(r'<a href="(/browseshop.phtml?owner=[\w*]&buy_obj_info_id=[\d*]&buy_cost_neopoints=[\d*])">')
            url = 'http://neopets.com{}'.format(link.group())
            resp = self.session_get(url)
            link = re.search(r'<A href="(buy_item.phtml?lower=0&owner=[\w*]&obj_info_id=[\d]&g=1&xhs=\w*&old_price=26000&feat=\d*,\d*,1&_ref_ck=\w*)" onClick=')
            url = 'http://neopets.com{}'.format(link.group())
            resp = self.session_get(url)

    def determine_course(self):
        url = 'http://www.neopets.com/island/fight_training.phtml?type=status'
        resp = self.session_get(url)
        level = int(re.search(r'(Lvl : <font color=green><b>)(\d*)', resp.text).group(2))
        strength = int(re.search(r'(Str : <b>)(\d*)', resp.text).group(2))
        defence = int(re.search(r'(Def : <b>)(\d*)', resp.text).group(2))
        hp = int(re.search(r'(Hp  : <b>)(\d*)', resp.text).group(2))

        if hp < (level * 2) - 20:
            course_type = 'Endurance'
            return course_type
        else:
            if strength and defence < (level * 2) - 20:
                if strength < defence:
                    course_type = 'Strength'
                    return course_type
                else:
                    course_type = 'Defence'
                    return course_type
            else:
                course_type = 'Level'
                return course_type

    def check_status_run(self):
        url = 'http://www.neopets.com/island/fight_training.phtml?type=status'
        resp = self.session_get(url)
        if 'Time till course finishes' in resp.text:
            print('Log: Already in course.')
            pass
        if 'This course has not been paid' in resp.text:
            self.make_payment()
            print('Log: Course has not been paid.')
        if 'Course Finished!' in resp.text:
            self.complete_course()
            print('Log: Course finished!')
            self.train_pet()
            self.make_payment()
            print('Log: {} is training {}.'.format(self.pet, self.course_type))
        else:
            self.train_pet()
            self.make_payment()
            print('Log: {} is training {}.'.format(self.pet, self.course_type))


    def train_pet(self):
        url = 'http://www.neopets.com/island/process_fight_training.phtml'
        self.session_post(url, data={'type': 'start', 'course_type': self.course_type, 'pet_name': self.pet})

    def make_payment(self):
        url = 'http://www.neopets.com/island/process_fight_training.phtml?type=pay&' \
              'pet_name={}'.format(self.pet)
        resp = self.session_get(url)
        if 'Time till course finishes :' in resp.text:
            return True

    def complete_course(self):
        url = 'http://www.neopets.com/island/process_fight_training.phtml'
        self.session_post(url, data={'type': 'complete', 'pet_name': self.pet})


def main():
    NeoSession()
    NinjaTrain()


if __name__ == '__main__':
    main()
    schedule.every(7).hours.do(main)

    while True:
        schedule.run_pending()
        time.sleep(random.randint(1000, 4000))
