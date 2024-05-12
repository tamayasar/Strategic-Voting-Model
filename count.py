from collections import OrderedDict 

votes = [-9, -7, -7, 1, 1, 3, 5, 5, 3, -9, 7, 7, 0, 7]
votes_set = set(votes)
#print(votes_set)

ordered = dict([(vote, votes.count(vote))
                for vote in votes_set])

print(ordered)
