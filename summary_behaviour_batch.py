import mesa
from strategic_voting import VotingModel
import pprint
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

width = 50
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

beh_names = ["tie", #0
             "left_suc_strategic", #1
             "left_unsuc_best_try", #2
             "left_unsuc_sincere", #3
             "left_unsuc_random", #4
             "left_winning_sincere", #5
             "right_suc_strategic", #6
             "right_unsuc_best_try", #7
             "right_unsuc_sincere", #8
             "right_unsuc_random", #9
             "right_winning_sincere"] #10

# Sincere indices
sii = [0, 5, 3, 10, 8]

# Strategic indices
sti = [1, 2, 6, 7]

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

sincere_list = []
strategic_list = []
for i in sii:
    sincere_list.append(means[i])
for i in sti:
    strategic_list.append(means[i])

sincere = [sum(i) for i in zip(*sincere_list)]
strategic = [sum(i) for i in zip(*strategic_list)]

# Save also the percentages.
percentage = max(strategic) / (width * width) * 100

f = open(f"radius4/summary_behaviour/percentages.txt", "a")
f.write(str(width) + " " + str(percentage) + "\n")
f.close()

plt.plot(sincere, label="sincere")
plt.plot(strategic, label="strategic")
plt.legend()
plt.savefig(f"deterministic/radius1/summary_behaviour/summary_behaviour-width{str(width)}.svg")
