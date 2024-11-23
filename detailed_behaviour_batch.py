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

# Get rid of symmetry.
results = [result for result in results
           if sum(list(result[-1].values())[4:9]) > sum(list(result[-1].values())[10:15])]

#pprint.pprint(results, sort_dicts=False)

beh_names = ["tie",
             "left_suc_strategic",
             "left_unsuc_best_try",
             "left_unsuc_sincere",
             "left_unsuc_random",
             "left_winning_sincere",
             "right_suc_strategic",
             "right_unsuc_best_try",
             "right_unsuc_sincere",
             "right_unsuc_random",
             "right_winning_sincere"]

ith_steps = lambda i : [result[i]["outcomes"] for result in results]
#pprint.pprint(ith_steps(0), sort_dicts=False)
behs = []
for k in range(11):
    behs.append([[list(outcomes.values())[k] for outcomes in ith_steps(i)] for i in range(steps+1)])
#pprint.pprint(tie, sort_dicts=False)
# [[1st ties],
#  [2nd ties],
#  ...       ,
#  [    ties]]

means = []
for i in range(11):
    means.append([mean(x) for x in behs[i]])

for i in range(11):
    plt.plot(means[i], label=str(beh_names[i]))
plt.legend()
plt.savefig(f"radius4/detailed_behaviour/detailed_behaviour-width{str(width)}-radius5.svg")
