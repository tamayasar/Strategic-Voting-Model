#!/usr/bin/env python
# coding: utf-8

import mesa
import seaborn as sns
import numpy as np
import pandas as pd
import random
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

# List of parties. Negative ones are left-wing, positive ones are
# right-wing. Bigger the absolute value, lesser the radicality of the
# party.
preferences = [-9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9]

weights = [1, 3, 5, 7, 9]

#colors = [(250, 187, 187), (250, 135, 135), (252, 101, 101), (250, 52, 52), (250, 15, 15), (0, 0, 0),
#          (15, 39, 250), (77, 95, 250), (130, 142, 250), (174, 182, 252), (214, 218, 255)]
#colors = [(e[0] / 255.0, e[1] / 255.0, e[2] / 255.0) for e in colors]
#cmap = ListedColormap(colors)

class Voter(mesa.Agent):
    """A voter with fixed initial preference."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preference = random.choice(preferences)
        self.next_preference = None

    def step(self):
        #print(f"Hi, I am a voter, you can call me {str(self.unique_id)}. I will vote to {str(self.preference)}.")
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False)
        #print(neighbors)
        neighbors_prefs = [neighbor.preference for neighbor in neighbors]
        #print(sum(neighbors_prefs))
        neighbors_sum = sum(neighbors_prefs)
        if neighbors_sum == 0: # It's a tie, then I vote sincerely.
            self.next_preference = self.preference
        elif neighbors_sum > 0: # Right-wing is winning, then I vote for the left-wing.
            for weight in weights:
                if neighbors_sum + (-weight) <= -4:
                    self.next_preference = -weight
                    #print(f"{str(self.pos)}, {str(neighbors_sum)}, {str(-weight)}")
                    break
            else:
                #self.next_preference = 9 # Left-wing will not win, but I will try my best.
                self.next_preference = self.preference
                #self.next_preference = random.choice(preferences)
        elif neighbors_sum < 0: # Left-wing is winning, then I vote for the right-wing.
            for weight in weights:
                if neighbors_sum + weight >= 4:
                    self.next_preference = weight
                    #print(f"{str(self.pos)}, {str(neighbors_sum)}, {str(weight)}")
                    break
            else:
                #self.next_preference = -9 # Right-wing will not win, but I will try my best.
                self.next_preference = self.preference
                #self.next_preference = random.choice(preferences)
    def advance(self):
        self.preference = self.next_preference

def count_preferences(model):
    preferences = [agent.preference for agent in model.schedule.agents]
    preferences_set = set(preferences)
    preferences = dict([(preference, preferences.count(preference))
                    for preference in preferences_set])

    return preferences[5]

class VotingModel(mesa.Model):
    """Model with some voters possibly voting strategically."""

    def __init__(self, width):
        super().__init__()
        self.num_voters = width * width
        self.grid = mesa.space.SingleGrid(width, width, True)
        self.schedule = mesa.time.SimultaneousActivation(self)

        # Create voters.
        for i in range(self.num_voters):
            a = Voter(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = a.unique_id % width
            y = a.unique_id // width
            self.grid.place_agent(a, (x, y))

        self.datacollector = mesa.DataCollector(
            model_reporters={"Votes": count_preferences},
            agent_reporters={"Preference": "preference"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

#elections = []
#
#votes = np.zeros((model.grid.width, model.grid.height))
#
#for voter, (x, y) in model.grid.coord_iter():
#    vote = voter.preference
#    votes[x][y] = vote
#
#votes = votes.T
#elections.append(votes)
#
#for i in range(150):
#    model.step()
#
#    votes = np.zeros((model.grid.width, model.grid.height))
#
#    for voter, (x, y) in model.grid.coord_iter():
#        vote = voter.preference
#        votes[x][y] = vote
#
#    votes = votes.T
#    elections.append(votes)
#
#for year, election in enumerate(elections):
#    g = sns.heatmap(election, cmap=cmap, annot=False, cbar=False, square=True)
#    plt.savefig(f"{str(year)}.png")
#    plt.clf()
