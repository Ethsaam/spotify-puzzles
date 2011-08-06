#!/usr/bin/env python3
# Bilateral Projects: http://www.spotify.com/se/jobs/tech/bilateral-projects/
# Peter Boström <pbos@kth.se> (2011-08-05)

# A Person is essentially an identifier and a list of teams
# they belong to, or might be needed in.
class Person:
	def __init__(self, number, team):
		self.number = number
		self.teams = [team]

	def __lt__(self, other):
		if len(self.teams) != len(other.teams):
			return len(self.teams) < len(other.teams)

		# Hunch says that this might be enough to help our friend out.
		# I've tried to provide counterexamples to this, but failed.
		# Probably because of restrictions put on the problem, that all
		# teams have exactly two members, etc.
		if self.number == 1009:
			return False
		if other.number == 1009:
			return True

		return self.number < other.number

# Parse input
num_teams = int(input())
teams = []
people = {}

# Read team pairs
for i in range(num_teams):
	(sth, ldn) = [int(i) for i in input().split()]

	teams.append([sth,ldn])

	def addperson(person, team):
		if person not in people:
			people[person] = Person(person, team)
		else:
			people[person].teams.append(team)

	addperson(sth, i)
	addperson(ldn, i)

# Start crunching
chosen = []
while len(people) != 0:
	# Removing a person will choose all people they're connected to, as
	# at least one person from each team needs to attend. It triggers a
	# chain reaction to remove all people who become redundant.
	def removeperson(p):
		del people[p.number]
		choose_ppl = []
		for team in p.teams:
			teams[team].remove(p.number)
			choose_ppl.append(teams[team][0])
		for c in choose_ppl:
			chooseperson(c)

	# Choosing a person will render some people unnecessary, which will in
	# turn remove them (continuing the chain reaction).
	def chooseperson(num):
		p = people[num]
		del people[num]
		# Register person as chosen
		chosen.append(num)
		remove_ppl = []
		# Remove person from all teams.
		for team in p.teams:
			teams[team].remove(num)
			# Remove co-worker from team as well, if they've not already
			# been removed from the team.
			if teams[team] != []:
				other = people[teams[team][0]]
				other.teams.remove(team)
				if other.teams == []:
					remove_ppl.append(other)
		# Finally, remove all people who are no longer required for any
		# teams.
		for p in remove_ppl:
			removeperson(p)

	# Remove person with least edges. This will only be our friend when
	# he's the last person with the fewest edges.
	rem = min(people.values())

	removeperson(rem)

# Print solution
print(len(chosen))

for c in chosen:
	print(c)
