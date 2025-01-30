import random
import time
import sys

def generate_shop_name():
    shop_set_before = ['Car Builder', 'Auto Works', 'Racing Garage', 
                'Auto Tuning House', 'Car Crafters',
                'Auto Works', 'Auto Tuning', 'Auto Works', 'Hot Rod Shop',
                'Import Tuner Shop', 'Tuning Garage', 'Tuner Shop']
    shop_set_after = ['Body Style Engineering', 'Car Creations', 'Auto Works', 'Performance Auto Solutions', 
                'Street Tuning', 'Racing Performance', 'Racing Innovations', 'Auto Styling', 'Car Tuning Unlimited', 
                'Street Legal Performance', 'Tuner Shop', 'Turbocharged Racing', 'Custom Car Kings']
    adj_list = ['High Performance', 'Total', 'Perfect', 'Ultimate', 'Supreme', 'Extreme', 'Speedy', 'Dream', 'Luxury', 'Superb', 'Elite', 'Custom', 'Fast Lane']
    with open('nounlist.txt') as f:
        noun_list = f.read().splitlines()
        noun = (random.choice(noun_list)).upper()
    if random.choice([True, False]):
        if random.choice([True, False]):
            shop_name = random.choice(adj_list) + " " + random.choice(shop_set_before) + " " + noun
        else:
            shop_name = random.choice(shop_set_before) + " " + noun
    else:
        if random.choice([True, False]):
            shop_name = noun + " " + random.choice(adj_list) + " " + random.choice(shop_set_after)
        else: 
            shop_name = noun + " " + random.choice(shop_set_after)
    return shop_name

while True:
    text = input()
    if text == 'q':
        break
    print(generate_shop_name())
    # if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    #   line = input()
    #   break