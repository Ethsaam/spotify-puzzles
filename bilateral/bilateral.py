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

#for town in (stockholm, london):
#	for person in town:
#		print(str(person.value) + ': ')
#		for p in person.neigh:
#			print('  ' + str(p.value))

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
		if k is None or v is None:
			continue
		out[k] = v
	return out

def flow_to_cover(match):
	vertices = copy(people)
	for (k, v) in match.items():
		del vertices[k.value]
	visited = {}
	q = deque()
	for (num, val) in vertices.items():
		visited[val] = True
		q.append((val, 0))

	cover = {}

	while q:
		(node, dist) = q.popleft()
		dist += 1
		for neigh in node.neigh:
			if neigh in visited:
				continue
			visited[neigh] = True
			q.append((neigh, dist))
			if dist & 1:
				cover[neigh.value] = True
				pair = match[neigh]
				del match[neigh]
				del match[pair]

	cover = list(cover.keys())
	for (k,v) in match.items():
		# if matched edge hasn't been used, prefer stockholm
		if k.value < v.value:
			cover.append(k.value)
	return cover

min_match = hopcroft_karp()
min_out = flow_to_cover(min_match)

if 1009 not in min_out and 1009 in people:
	# attempt another vertex cover, which includes our
	# friend, if it's still minimum, use it
	friend = people[1009]
	for n in friend.neigh:
		n.neigh.remove(friend)

	friend.neigh = []

	friend_match = hopcroft_karp()
	friend_out = flow_to_cover(friend_match)
	friend_out.append(1009)

	if len(friend_out) == len(min_out):
		min_out = friend_out

print(min_out)
