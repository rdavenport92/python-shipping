import pytest

import main

# weighs 12 pounds, what's the cheapest way to ship?


@pytest.mark.parametrize(
    'pounds,calculated_shipping',
    [
        (2, 9),
        (4, 36),
        (10, 120),
        (420, 5985)
    ]
)
def test_best_shipping_deal_finder_finds_best_shipping_deal():
    return


@pytest.mark.parametrize(
    'pounds,calculated_shipping',
    [
        (2, 9),
        (4, 36),
        (10, 120),
        (420, 5985)
    ]
)
def test_drone_calc_gives_correct_shipping_costs(pounds, calculated_shipping):
    """Test that pounds result in accurate shipping cost for drone."""
    result = main.shipping_calculator(
        main.drone_shipping_config,
        pounds=pounds
    )

    assert result == calculated_shipping


@pytest.mark.parametrize(
    'pounds,calculated_shipping',
    [
        (1, 1.50),
        (2, 3),
        (3, 9),
        (8, 32),
        (10, 40),
        (11, 52.25),
        (65948135, 313253641.25)
    ]
)
def test_ground_calc_gives_correct_shipping_costs(pounds, calculated_shipping):
    """Test that pounds result in accurate shipping cost for ground."""
    result = main.shipping_calculator(
        main.ground_shipping_config,
        pounds=pounds
    )

    flat_rate = main.ground_shipping_config.flat_rate
    assert result == calculated_shipping + flat_rate


def test_premium_calc_gives_correct_shipping_costs():
    """Test that pounds result in accurate shipping cost for premium."""
    result = main.shipping_calculator(main.premium_shipping_config, pounds=45)

    assert result == main.premium_shipping_config.flat_rate
