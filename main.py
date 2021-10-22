import enum
from typing import List
import copy
import os


class ShippingType(enum.Enum):
    GROUND = 'ground'
    DRONE = 'drone'
    PREMIUM = 'premium'


class ShippingConfig:
    shipping_multiplier = None

    def __init__(
        self,
        type: ShippingType,
        flat_rate=0,
        shipping_multiplier=None
    ):
        self.type = type
        self.flat_rate = flat_rate
        if shipping_multiplier:
            self.shipping_multiplier = shipping_multiplier


def ground_shipping_multiplier(pounds):
    multiplier = 0

    if pounds <= 2:
        multiplier = 1.5
    elif pounds > 2 and pounds <= 6:
        multiplier = 3
    elif pounds > 6 and pounds <= 10:
        multiplier = 4
    else:
        multiplier = 4.75

    return pounds * multiplier


def drone_shipping_multiplier(pounds):
    multiplier = 0

    if pounds <= 2:
        multiplier = 4.50
    elif pounds > 2 and pounds <= 6:
        multiplier = 9
    elif pounds > 6 and pounds <= 10:
        multiplier = 12
    else:
        multiplier = 14.25

    return pounds * multiplier


def shipping_calculator(
    shipping_config: ShippingConfig,
    pounds=0
) -> int:
    total_shipping = 0

    if shipping_config.shipping_multiplier:
        total_shipping += shipping_config.shipping_multiplier(pounds)

    total_shipping += shipping_config.flat_rate
    return total_shipping


def best_shipping_deal_finder(
    pounds,
    shipping_config_options: List[ShippingConfig]
):
    best_deal = {
        'shipping_total': None,
        'shipping_config_type': None
    }
    all_deals = []

    for shipping_config in shipping_config_options:
        current_option_shipping = shipping_calculator(
            shipping_config, pounds=pounds
        )

        current_deal = {
            'shipping_total': current_option_shipping,
            'shipping_config_type': shipping_config.type.value
        }
        all_deals.append(current_deal)

        if best_deal['shipping_total'] is None \
                or current_option_shipping < best_deal['shipping_total']:
            best_deal = copy.deepcopy(current_deal)

    return {'best_deal': best_deal, 'all_deals': all_deals}


def format_output(best_deal_result):
    def format_currency(shipping):
        return "${:,.2f}".format(shipping)

    best_total = best_deal_result['best_deal']['shipping_total']
    best_type: str = best_deal_result['best_deal']['shipping_config_type']

    print(
        f"""Based on your product's weight, here is your best shipping option:

        Type: {best_type.capitalize()}
        Total: {format_currency(best_total)}\n\n""")
    print('All options:\n')
    print('------\n')
    for option in best_deal_result['all_deals']:
        shipping_type = option['shipping_config_type']
        shipping_total = option['shipping_total']
        print(f"Type: {shipping_type.capitalize()}")
        print(f"Shipping: {format_currency(shipping_total)}")
        print('\n------\n')


ground_shipping_config = ShippingConfig(
    ShippingType.GROUND,
    flat_rate=20,
    shipping_multiplier=ground_shipping_multiplier
)

premium_shipping_config = ShippingConfig(
    ShippingType.PREMIUM,
    flat_rate=125
)

drone_shipping_config = ShippingConfig(
    ShippingType.DRONE,
    shipping_multiplier=drone_shipping_multiplier
)

SHIPPING_OPTIONS = [
    ground_shipping_config,
    premium_shipping_config,
    drone_shipping_config
]


def main():
    while True:
        os.system('cls')
        pounds = input('What is your weight? (Press "q" to quit.): ')
        if pounds == 'q':
            return
        try:
            pounds = int(pounds)
            result = best_shipping_deal_finder(pounds, SHIPPING_OPTIONS)
            format_output(result)
        except Exception as err:
            print('Pounds must be a number!', err)
        finally:
            input('Press enter to continue')


if __name__ == '__main__':
    main()
