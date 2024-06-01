class Customer:
    def __init__(self, customer_id, name, postcode="", phone_number=""):
        self.customer_id = customer_id
        self.name = name
        self.postcode = postcode
        self.phone_number = phone_number
        self.sales = []


class Sale:
    def __init__(self, sale_id, customer_id, date, category, value):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.date = date
        self.category = category
        self.value = value
