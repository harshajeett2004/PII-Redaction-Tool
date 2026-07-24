from faker import Faker
import random
import ipaddress
import re
from urllib.parse import urlparse

fake = Faker("en_IN")


class FakeDataGenerator:
    """
    Generates realistic fake data while maintaining
    consistent replacements throughout the document.
    """

    def __init__(self):

        self.person_map = {}
        self.email_map = {}
        self.phone_map = {}
        self.company_map = {}
        self.address_map = {}
        self.url_map = {}
        self.ip_map = {}
        self.date_map = {}
        self.pan_map = {}
        self.card_map = {}

    # -------------------------------
    # PERSON
    # -------------------------------

    def fake_person(self, original):

        if original not in self.person_map:
            self.person_map[original] = fake.name()

        return self.person_map[original]

    # -------------------------------
    # EMAIL
    # -------------------------------

    def fake_email(self, original):

        if original not in self.email_map:
            self.email_map[original] = fake.email()

        return self.email_map[original]

    # -------------------------------
    # PHONE
    # -------------------------------

    def fake_phone(self, original):

        if original not in self.phone_map:

            number = "9"

            for _ in range(9):
                number += str(random.randint(0, 9))

            self.phone_map[original] = "+91 " + number

        return self.phone_map[original]

    # -------------------------------
    # COMPANY
    # -------------------------------

    def fake_company(self, original):

        if original not in self.company_map:
            self.company_map[original] = fake.company()

        return self.company_map[original]

    # -------------------------------
    # ADDRESS
    # -------------------------------

    def fake_address(self, original):

        if original not in self.address_map:

            address = fake.address()

            address = address.replace("\n", ", ")

            self.address_map[original] = address

        return self.address_map[original]

    # -------------------------------
    # URL
    # -------------------------------

    def fake_url(self, original):

        if original not in self.url_map:

            parsed = urlparse(original)

            scheme = parsed.scheme if parsed.scheme else "https"

            domain = fake.domain_name()

            self.url_map[original] = f"{scheme}://{domain}"

        return self.url_map[original]

    # -------------------------------
    # IP ADDRESS
    # -------------------------------

    def fake_ip(self, original):

        if original not in self.ip_map:

            ip = ipaddress.IPv4Address(
                random.randint(0, 2 ** 32 - 1)
            )

            self.ip_map[original] = str(ip)

        return self.ip_map[original]

    # -------------------------------
    # DATE
    # -------------------------------

    def fake_date(self, original):

        if original not in self.date_map:
            self.date_map[original] = str(fake.date())

        return self.date_map[original]

    # -------------------------------
    # PAN NUMBER
    # -------------------------------

    def fake_pan(self, original):

        if original not in self.pan_map:

            letters = "".join(
                random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                for _ in range(5)
            )

            digits = "".join(
                str(random.randint(0, 9))
                for _ in range(4)
            )

            last = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

            self.pan_map[original] = letters + digits + last

        return self.pan_map[original]

    # -------------------------------
    # CREDIT CARD
    # -------------------------------

    def fake_credit_card(self, original):

        if original not in self.card_map:

            number = ""

            for i in range(16):

                number += str(random.randint(0, 9))

                if i in [3, 7, 11]:
                    number += " "

            self.card_map[original] = number

        return self.card_map[original]

    # -------------------------------
    # Generic Function
    # -------------------------------

    def generate(self, entity_type, original):

        entity_type = entity_type.upper()

        if entity_type == "PERSON":
            return self.fake_person(original)

        elif entity_type == "EMAIL":
            return self.fake_email(original)

        elif entity_type == "PHONE":
            return self.fake_phone(original)

        elif entity_type == "COMPANY":
            return self.fake_company(original)

        elif entity_type == "ADDRESS":
            return self.fake_address(original)

        elif entity_type == "URL":
            return self.fake_url(original)

        elif entity_type == "IP":
            return self.fake_ip(original)

        elif entity_type == "DATE":
            return self.fake_date(original)

        elif entity_type == "PAN":
            return self.fake_pan(original)

        elif entity_type == "CREDIT_CARD":
            return self.fake_credit_card(original)

        return "[REDACTED]"


# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    generator = FakeDataGenerator()

    print("\nTesting Fake Data Generator\n")

    print("Person:")
    print(generator.generate("PERSON", "Rajesh Kumar"))
    print(generator.generate("PERSON", "Rajesh Kumar"))

    print("\nEmail:")
    print(generator.generate("EMAIL", "abc@gmail.com"))

    print("\nPhone:")
    print(generator.generate("PHONE", "+91 9876543210"))

    print("\nCompany:")
    print(generator.generate("COMPANY", "Infosys Ltd"))

    print("\nAddress:")
    print(generator.generate("ADDRESS", "Kolkata"))

    print("\nURL:")
    print(generator.generate("URL", "https://google.com"))

    print("\nIP:")
    print(generator.generate("IP", "192.168.1.1"))

    print("\nDate:")
    print(generator.generate("DATE", "12/12/2024"))

    print("\nPAN:")
    print(generator.generate("PAN", "ABCDE1234F"))

    print("\nCredit Card:")
    print(generator.generate("CREDIT_CARD", "1234 5678 9012 3456"))