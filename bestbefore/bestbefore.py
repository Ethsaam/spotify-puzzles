#!/usr/bin/env python3
import datetime
import itertools
import sys

line = input()

nums = line.split('/')

#validate input
error = False
if len(nums) is not 3:
	error = True
else:
	for num in nums:
		if len(num) not in [1,2,4]:
			error = True
			break
if error:
	print(line, 'is illegal')
	sys.exit(1)
assert len(nums) == 3

earliest = None
for perm in itertools.permutations(nums):
	year = perm[0]
	if len(year) < 4:
		year = 2000 + int(year)

	month = int(perm[1])
	day = int(perm[2])
	try:
		date = datetime.date(year, month, day)
		if earliest is None or date < earliest:
			earliest = date
	except ValueError:
		pass

if earliest is None:
	print(line, 'is illegal')
	sys.exit(1)
else:
	print(earliest.isoformat())
