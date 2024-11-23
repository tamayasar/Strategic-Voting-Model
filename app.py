import solara
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from strategic_voting import VotingModel, preferences
from mesa.experimental import JupyterViz

colors = ["#fabbbb", "#f78f8f", "#f75c5c", "#f52a2a", "#ff0000", "#000000",
          "#023cf7", "#2a5af7", "#4f77f7", "#7997f7", "#93abfa"]

def agent_portrayal(agent):
    #portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    color = colors[preferences.index(agent.preference)]
    return {
            "shape": "square",
            "color": color,
            "size": 30,
            }

def scale(model):
    fig = Figure()
    ax = fig.subplots()
    scale = mpimg.imread("scale.png")
    ax.axis('off')
    imgplot = ax.imshow(scale)
    ax.set_title("Representation of the Parties")
    solara.FigureMatplotlib(fig)

def piechart(model):
    fig = Figure()
    ax = fig.subplots()
    data = model.datacollector.get_model_vars_dataframe()
    #print(data)
    if data.size > 0:
        data = data.iloc[-1]
        # Votes are in the first 11 column.
        data = data[:11]
        #print(data)
        ax.pie(data.values, labels=data.index, colors=colors, autopct='%1.1f%%')
        ax.set_title("Voter Distribution")
        solara.FigureMatplotlib(fig)

def time_series(model):
    fig = Figure()
    ax = fig.subplots()
    data = model.datacollector.get_model_vars_dataframe()
    #print(data.columns.tolist())
    if data.size > 0:
        for i, p in enumerate(preferences):
            ax.plot(data.iloc[:, i].values, color=colors[i])
        ax.set_title("Evolution of Popularity of Preferences")
        solara.FigureMatplotlib(fig)

def outcomes(model):
    fig = Figure()
    ax = fig.subplots()
    data = model.datacollector.get_model_vars_dataframe()
    if data.size > 0:
        data = data.iloc[:, -1]
        for key in data[0]:
            if key != "left_winning_sincere" and key != "right_winning_sincere":
                series = [gen[key] for gen in data.values]
                ax.plot(series, label=key)
        ax.set_title("Evolution of Voter Behaviour (Detailed)")
        ax.legend()
        solara.FigureMatplotlib(fig)

def sincere_strategic(model):
    fig = Figure()
    ax = fig.subplots()
    data = model.datacollector.get_model_vars_dataframe()
    if data.size > 0:
        data = data.iloc[:, -1]
        # tie
        # left_winning_sincere
        # left_unsuc_sincere
        # right_winning_sincere
        # right_unsuc_sincere
        # ---
        # left_suc_strategic
        # left_unsuc_best_try
        # right_suc_strategic
        # right_unsuc_best_try
        # ---
        # right_unsuc_random
        # left_unsuc_random
        tie = [gen["tie"] for gen in data.values]
        left_winning_sincere = [gen["left_winning_sincere"] for gen in data.values]
        left_unsuc_sincere = [gen["left_unsuc_sincere"] for gen in data.values]
        right_winning_sincere = [gen["right_winning_sincere"] for gen in data.values]
        right_unsuc_sincere = [gen["right_unsuc_sincere"] for gen in data.values]
        sincere_list = [tie, left_winning_sincere, left_unsuc_sincere,
                        right_winning_sincere, right_unsuc_sincere]

        left_suc_strategic = [gen["left_suc_strategic"] for gen in data.values]
        left_unsuc_best_try = [gen["left_unsuc_best_try"] for gen in data.values]
        right_suc_strategic = [gen["right_suc_strategic"] for gen in data.values]
        right_unsuc_best_try = [gen["right_unsuc_best_try"] for gen in data.values]
        strategic_list = [left_suc_strategic, left_unsuc_best_try,
                          right_suc_strategic, right_unsuc_best_try]

        sincere = [sum(i) for i in zip(*sincere_list)]
        strategic = [sum(i) for i in zip(*strategic_list)]
        print("Sincere", sincere)
        print("Strategic", strategic)
        ax.plot(sincere, label="Sincere votes")
        ax.plot(strategic, label="Strategic votes")
        ax.set_title("Evolution of Voter Behaviour (Summary)")
        ax.legend()
        solara.FigureMatplotlib(fig)

model_params = {
        "width": {
            "type": "SliderInt",
            "value": 40,
            "label": "Grid Width: ",
            "min": 10,
            "max": 100,
            "step": 5,
            }
        }

page = JupyterViz(
        VotingModel,
        model_params,
        #measures=["-1", "-3", "-5", "-7", "-9", "0", "1", "3", "5", "7", "9"],
        measures=[scale, piechart, time_series, outcomes, sincere_strategic],
        name="Strategic Voting Model",
        agent_portrayal=agent_portrayal,
        )
