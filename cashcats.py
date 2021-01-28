import csv
import sys
import time
from bookingdata import BookingList

if len(sys.argv) < 2:
	sys.exit("cashcats.py [csv file] [csv file 2]...")

bookings = BookingList()
booking_count = [0, 0]

for csv_file in sys.argv:
	if csv_file.find(".csv") == -1 and  csv_file.find(".CSV") == -1:
		continue
	with open(csv_file, "r", encoding="ISO-8859-1") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')

		first_line = True
		bank_type = "Sparkasse"

		for row in csv_reader:
			if first_line:
				first_line = False
				if row[1] == "Belegdatum":
					bank_type = "Master Card"
			else:
				res = False
				if bank_type == "Sparkasse":
					res = bookings.add_booking(row[11], row[14], row[4])
				elif bank_type == "Master Card":
					res = bookings.add_booking(row[8], row[3], row[8])
				if res == True:
					booking_count[0] += 1
				else:
					booking_count[1] += 1

print(f"\n\nsuccess / failed {booking_count[0]} / {booking_count[1]} \n\n")
bookings.print_bookings()

resfile = "res" + time.strftime("%Y%m%d-%H%M%S") + ".csv"

with open(resfile, 'w', newline='') as csvfile:
    reswriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    reswriter.writerow(["section", "sum"])
    bookings.enumerate(reswriter.writerow)
