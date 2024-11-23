from functools import partial
import random
import mesa
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import pprint

# List of parties. Negative ones are left-wing, positive ones are
# right-wing. Radical parties have higher weight.
left = [-9, -7, -5, -3, -1]
right = [1, 3, 5, 7, 9]
preferences = left + [0] + right
preferences_p = left + right

# Keep also names.
names = ["E", "D", "C", "B", "A", "O", "A'", "B'", "C'", "D'", "E'"]

weights = [1, 3, 5, 7, 9]

colors = [(250, 187, 187), (250, 135, 135), (252, 101, 101), (250, 52, 52), (250, 15, 15), (0, 0, 0),
          (15, 39, 250), (77, 95, 250), (130, 142, 250), (174, 182, 252), (214, 218, 255)]

colors = [(e[0] / 255.0, e[1] / 255.0, e[2] / 255.0) for e in colors]
cmap = ListedColormap(colors)

def portions(n):
    a = random.sample(range(1, n), 4) + [0, n]
    list.sort(a)
    return sorted([a[i + 1] - a[i] for i in range(len(a) - 1)])

class Voter(mesa.Agent):
    """A voter with fixed initial preference."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preference = random.choice(preferences)
        #self.preference = model.voters.pop()
        #self.preference = random.choices(preferences, left_portions + [4]
        #                                 + right_portions)[0]
        self.next_preference = None

    def step(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=False,
            radius=1)
        #print(neighbors)
        neighbors_prefs = [neighbor.preference for neighbor in neighbors]
        #print(sum(neighbors_prefs))
        neighbors_sum = sum(neighbors_prefs)
        if neighbors_sum == 0: # It's a tie, then I vote sincerely.
            self.next_preference = self.preference
            self.model.outcomes["tie"] += 1
        elif neighbors_sum > 0:
            # Right-wing is winning. If I am a rightist, then I vote
            # sincerely, otherwise I vote strategically.
            if self.preference < 0:
                for weight in weights:
                    if neighbors_sum + self.preference <= 0:
                        self.next_preference = self.preference
                        break
                    if neighbors_sum + (-weight) <= 0:
                        self.next_preference = -weight
                        self.model.outcomes["left_suc_strategic"] += 1
                        #print(f"{str(self.pos)}, {str(neighbors_sum)}, {str(-weight)}")
                        break
                else:
                    #toss = random.choice([-1, 0, 1])
                    toss = random.choice([-1])
                    if toss == -1:
                        self.next_preference = -9 # Left-wing will not win, but I will try my best.
                        self.model.outcomes["left_unsuc_best_try"] += 1
                    elif toss == 0:
                        self.next_preference = self.preference
                        self.model.outcomes["left_unsuc_sincere"] += 1
                    elif toss == 1:
                        self.next_preference = random.choice(preferences_p)
                        self.model.outcomes["left_unsuc_random"] += 1
            else:
                self.next_preference = self.preference
                self.model.outcomes["right_winning_sincere"] += 1
        elif neighbors_sum < 0:
            # Left-wing is winning. If I am a leftist, then I vote
            # sincerely, otherwise I vote strategically.
            if self.preference > 0:
                for weight in weights:
                    if neighbors_sum + self.preference >= 0:
                        self.next_preference = self.preference
                        break
                    if neighbors_sum + weight >= 0:
                        self.next_preference = weight
                        self.model.outcomes["right_suc_strategic"] += 1
                        #print(f"{str(self.pos)}, {str(neighbors_sum)}, {str(weight)}")
                        break
                else:
                    #toss = random.choice([-1, 0, 1])
                    toss = random.choice([-1])
                    if toss == -1:
                        self.next_preference = 9 # Left-wing will not win, but I will try my best.
                        self.model.outcomes["right_unsuc_best_try"] += 1
                    elif toss == 0:
                        self.next_preference = self.preference
                        self.model.outcomes["right_unsuc_sincere"] += 1
                    elif toss == 1:
                        self.next_preference = random.choice(preferences_p)
                        self.model.outcomes["right_unsuc_random"] += 1
            else:
                self.next_preference = self.preference
                self.model.outcomes["left_winning_sincere"] += 1

    def advance(self):
        self.preference = self.next_preference

# Construct the reporter dictionary.
def count_preferences(model, preference):
    prefs_list = [agent.preference for agent in model.schedule.agents]
    prefs_set = set(preferences)
    prefs_dict = dict([(preference, prefs_list.count(preference))
                       for preference in prefs_set])

    return prefs_dict[preference]

model_reporters = {str(names[i]): partial(count_preferences,
                                            preference=preference) for
                   i, preference in enumerate(preferences)}

# Add the outcomes reporter.
model_reporters["outcomes"] = lambda m : dict(m.outcomes)

class VotingModel(mesa.Model):
    """Model with some voters possibly voting strategically."""

    def __init__(self, width):
        super().__init__()
        self.num_voters = width * width

        self.grid = mesa.space.SingleGrid(width, width, True)
        self.schedule = mesa.time.SimultaneousActivation(self)

        # Keep count of sincere and strategic votes.
        self.outcomes = {
                "tie" : 0,
                "left_suc_strategic" : 0,
                "left_unsuc_best_try" : 0,
                "left_unsuc_sincere" : 0,
                "left_unsuc_random" : 0,
                "left_winning_sincere" : 0,
                "right_suc_strategic" : 0,
                "right_unsuc_best_try" : 0,
                "right_unsuc_sincere" : 0,
                "right_unsuc_random" : 0,
                "right_winning_sincere" : 0,
                }

        # Initiate portions of the parties
        #left_portions = sorted(portions(48), reverse=True)
        #right_portions = portions(48)

        #print(left_portions, right_portions)

        #self.voter_portions = left_portions + [4] + right_portions
        #self.voters = []
        #for index, i in enumerate(self.voter_portions):
        #    # Assume width is a multiple of 10.
        #    for _ in range(i * self.num_voters // 100):
        #        self.voters.append(preferences[index])

        # Create voters.
        for i in range(self.num_voters):
            voter = Voter(i, self)
            self.schedule.add(voter)

            # Place the agent to a random grid cell
            self.grid.place_agent(voter, random.choice(list(self.grid.empties)))

        self.datacollector = mesa.DataCollector(model_reporters=model_reporters)

    def step(self):
        self.datacollector.collect(self)
        # Reset outcomes counters.
        for key in self.outcomes:
            self.outcomes[key] = 0
        self.schedule.step()
