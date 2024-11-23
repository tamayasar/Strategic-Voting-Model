from strategic_voting import VotingModel
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib

levels = [-10, -8, -6, -4, -2, -0.5, 0.5, 2, 4, 6, 8, 10]

colors = [(250, 187, 187), (250, 135, 135), (252, 101, 101), (250, 52, 52), (250, 15, 15), (0, 0, 0),
          (15, 39, 250), (77, 95, 250), (130, 142, 250), (174, 182, 252), (214, 218, 255)]

colors = [(e[0] / 255.0, e[1] / 255.0, e[2] / 255.0) for e in colors]
#cmap = ListedColormap(colors)
cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors)

width = 100
model = VotingModel(width)

elections = []

votes = np.zeros((model.grid.width, model.grid.height))

for voter, (x, y) in model.grid.coord_iter():
    vote = voter.preference
    votes[x][y] = vote

votes = votes.T
elections.append(votes)

for i in range(50):
    model.step()

    votes = np.zeros((model.grid.width, model.grid.height))

    for voter, (x, y) in model.grid.coord_iter():
        vote = voter.preference
        votes[x][y] = vote

    votes = votes.T
    elections.append(votes)

for year, election in enumerate(elections):
    g = sns.heatmap(election, cmap=cmap, norm=norm, annot=False, cbar=False, square=True)
    plt.axis('off')
    plt.savefig(f"plots/radius4/{str(width)}/{str(year)}.svg", bbox_inches='tight')
    plt.clf()
