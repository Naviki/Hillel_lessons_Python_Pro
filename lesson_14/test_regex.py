import re
import pytest

passport_pattern = re.compile(r"^[А-ЩЬЮЯҐЄІЇ]{2}\d{6}$")
ipn_pattern = re.compile(r"^\d{10}$")
car_number_pattern = re.compile(r"^(АЕ|АХ)\d{4}[А-ЩЬЮЯҐЄІЇ]{2}$")

test_passports = ["ТТ778899", "АБ123456", "ВЇ654321"]
test_ipns = ["1234567890", "9876543210", "5555555555"]
test_car_numbers = ["АЕ1234БВ", "АХ5678ДЖ", "АХ9999ЄІ"]

def test_passport_pattern():
    for passport in test_passports:
        assert passport_pattern.match(passport), f"Failed on {passport}"

def test_ipn_pattern():
    for ipn in test_ipns:
        assert ipn_pattern.match(ipn), f"Failed on {ipn}"

def test_car_number_pattern():
    for car_number in test_car_numbers:
        assert car_number_pattern.match(car_number), f"Failed on {car_number}"

if __name__ == "__main__":
    pytest.main()
