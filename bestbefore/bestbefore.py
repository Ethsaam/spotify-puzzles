#!/usr/bin/env python3
# Best Before: http://www.spotify.com/se/jobs/tech/best-before/
# Peter Boström <pbos@kth.se> (2011-08-03)

import datetime
import itertools
import sys

# Read input
line = input()
nums = line.split('/')

# Validate input
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

# Try all permutations for the date, simple
# solution. Let datetime.date check if it's
# valid, simply.
earliest = None
for perm in itertools.permutations(nums):
	year = int(perm[0])
	if year < 1000:
		year += 2000

	month = int(perm[1])
	day = int(perm[2])
	try:
		date = datetime.date(year, month, day)
		if earliest is None or date < earliest:
			earliest = date
	except ValueError:
		pass

# Print results
if earliest is None:
	print(line, 'is illegal')
	sys.exit(1)
else:
	print(earliest.isoformat())
