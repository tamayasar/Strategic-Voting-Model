import mesa
from strategic_voting import VotingModel
import pprint
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

width = 100
steps = 50
iters = 200
params = {"width": width}

results = mesa.batch_run(
        VotingModel,
        parameters=params,
        max_steps=steps,
        iterations=iters,
        data_collection_period=1,
        number_processes=8,
        )

#print(len(results))
#pprint.pprint(results, sort_dicts=False)

#results_df = pd.DataFrame(results)
#print(results_df)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

results = list(chunks(results, steps+1))

#pprint.pprint(results[1][-1], sort_dicts=False)
#print(results[0][0].values())
#print(list(results[0][0].values())[4:15])
#print(list(results[0][0].values())[4])
#print(list(results[0][0].values())[14])

#for k in results[0]:
#    print(list(k.values())[4:15])

#for i in results:
#    for k in i:
#        print(list(k.values())[4:15])

results = [result for result in results
           if sum(list(result[-1].values())[4:9]) > sum(list(result[-1].values())[10:15])]

ith_steps = lambda i : [list(result[i].values())[4:15] for result in results]
means_of_steps = [[mean(x) for x in zip(*ith_steps(i))] for i in range(steps+1)]

pop_evos = np.matrix(means_of_steps).T

names = ["E", "D", "C", "B", "A", "O", "A'", "B'", "C'", "D'", "E'"]

colors = [(250, 187, 187), (250, 135, 135), (252, 101, 101), (250, 52, 52), (250, 15, 15), (0, 0, 0),
          (15, 39, 250), (77, 95, 250), (130, 142, 250), (174, 182, 252), (214, 218, 255)]

colors = [(e[0] / 255.0, e[1] / 255.0, e[2] / 255.0) for e in colors]

for i in range(len(names)):
    plt.plot(pop_evos[i].T, color=colors[i])
plt.savefig(f"radius4/pops/pop-width{str(width)}.svg")
