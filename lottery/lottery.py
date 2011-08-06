#!/usr/bin/env python3
# Ticket Lottery: http://www.spotify.com/se/jobs/tech/ticket-lottery/
# Peter Boström <pbos@kth.se> (2011-08-04)
import math

# Binomial coefficient (n choose k)
def choose(n, k):
	if k < 0 or k > n:
		return 0
	if k > n - k:
		k = n - k
	c = 1
	for i in range(k):
		c *= (n - i)
		c = c // (i + 1)
	return c

# m people who entered the lottery
# n winners drawn
# t tickets the winner may buy
# p people in your group

(m, n, t, p) = [int(i) for i in input().split()]

# If we need to buy p tickets, and each winner gets
# to buy t tickets, we need p/t winners, rounded up.
needed_wins = int(math.ceil(p/t))

# How many lots we have.
ours = p
# How many lots we don't have (they, others, have).
theirs = m - p
# How many lots are drawn.
draws = n

# Counting losses
loss = 0

# We 'lose' whenever less than needed_wins tickets
# from our side is drawn. Iterate [0, needed_wins)
# and count configurations of this happening.
for i in range(needed_wins):
	loss += choose(theirs, draws-i) * choose(ours, i)

# Then compare to total number of configurations
total = choose(m, n)

prob = 1 - loss / total

print(prob)
