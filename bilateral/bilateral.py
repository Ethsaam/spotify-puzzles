#!/usr/bin/env python3
# Bilateral Projects: http://www.spotify.com/se/jobs/tech/bilateral-projects/
# Peter Boström <pbos@kth.se> (2012-01-10)
from collections import deque
from copy import copy

class Node:
	def __init__(self, value):
		self.value = value
		self.neigh = []

# Parse input
num_teams = int(input())
people = {}
stockholm = []
london = []

# Read team pairs
for i in range(num_teams):
	(sth, ldn) = [int(j) for j in input().split()]

	for person in [sth,ldn]:
		if person not in people:
			node = Node(person)
			people[person] = node
			if person == sth:
				stockholm.append(node)
			else:
				london.append(node)

	people[sth].neigh.append(people[ldn])
	people[ldn].neigh.append(people[sth])

for town in (stockholm, london):
	for person in town:
		print(str(person.value) + ': ')
		for p in person.neigh:
			print('  ' + str(p.value))

# straight(ish) out of wikipedia
def hopcroft_karp():
	def bfs():
		q = deque()
		for v in stockholm:
			if pair[v] is None:
				dist[v] = 0
				q.append(v)
			else:
				dist[v] = None

		dist[None] = None
		while q:
			v = q.popleft()
			if v is None:
				continue
			for u in v.neigh:
				if dist[pair[u]] == None:
					dist[pair[u]] = dist[v] + 1
					q.append(pair[u])

		return dist[None] != None

	def dfs(v):
		if v == None:
			return True
		for u in v.neigh:
			if dist[pair[u]] == dist[v] + 1:
				if dfs(pair[u]):
					pair[u] = v
					pair[v] = u
					return True
		dist[v] = None
		return False
	pair = {None: None}
	for (number, v) in people.items():
		pair[v] = None
	dist = {}
	matching = 0
	while bfs():
		for v in stockholm:
			if pair[v] == None:
				if dfs(v):
					matching += 1

	out = {}
	for k, v in pair.items():
		if k is None or v is None or k.value > v.value:
			continue
		out[k] = v
	return out

def flow_to_cover(match):
	vertices = copy(people)
	for (k, v) in match.items():
		del vertices[k.value]
		del vertices[v.value]
	return [str(a.value) + ': ' + str(b.value) for (a,b) in match.items()]

min_match = hopcroft_karp()
for k, v in min_match.items():
	print(str(k.value) + ': ' + str(v.value))

min_out = flow_to_cover(min_match)

print(min_out)
