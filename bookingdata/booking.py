import re

def combi_bargeld_cb(bookingList, amount, usage):
	result = re.search('Bargeldausz. (.*) EUR', usage)
	overall_amount = bookingList.parse_amount(amount)
	bar_amount = bookingList.parse_amount(result.group(1)) * -1


	bookingList._add_booking(bar_amount, "Bargeldauszahlung Supermarkt")
	bookingList._add_booking(overall_amount-bar_amount, "Supermarkt")

# modify as you need
SECTION_MAP = [
	{"name": "ignore", "usage_marks": ["Ihr Einkauf bei SPOTIFY "]},
	{"name": "Lieferando", "usage_marks": ["TAKEAWAYCOM", "Lieferando.de"]},
	{"name": "Bargeldauszahlung Supermarkt", "usage_marks": ["Bargeldausz. "], "usage_cb": combi_bargeld_cb},
	{"name": "Sonstige Paypal",  "usage_marks": ["Ihr Einkauf bei "]},
]

class BookingList:
	def __init__(self):
		self.bookings = {}

	def parse_amount(self, amount):
		if isinstance(amount, str):
			amount = amount.replace(",", ".")
		return float(amount)

	def _add_booking(self, amount, name):
		if name == "ignore":
			return

		amount = self.parse_amount(amount)
		if amount > 0:
			return
		if name in self.bookings:
			self.bookings[name] += amount
		else:
			self.bookings[name] = amount
		print(f"+ {name} -> {amount} EUR")

	def add_booking(self, recveiver, amount, usage):
		for sd in SECTION_MAP:
			if "recveiver_marks" in sd:
				for rm in sd["recveiver_marks"]:
					if recveiver.find(rm) != -1:
						self._add_booking(amount, sd["name"])
						return True
			if "usage_marks" in sd:
				for um in sd["usage_marks"]:
					if usage.find(um) != -1:
						if "usage_cb" in sd:
							sd["usage_cb"](self, amount, usage)
						else:
							self._add_booking(amount, sd["name"])

						return True
		self._add_booking(amount, "Nicht zugeordnet")
		print(f"- {recveiver} -> {amount} EUR")
		return False

	def print_bookings(self):
		for name in self.bookings:
			print(f"{name}: {self.bookings[name]}")

	def enumerate(self, f):
		for name in self.bookings:
			f([name, round(self.bookings[name], 2)])
