import mesa
from strategic_voting import VotingModel
from strategic_voting import preferences
from mesa.experimental import JupyterViz

colors = ["#fabbbb", "#f78f8f", "#f75c5c", "#f52a2a", "#ff0000", "#000000",
          "#023cf7", "#2a5af7", "#4f77f7", "#7997f7", "#93abfa"]

def agent_portrayal(agent):
    #portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    color = colors[preferences.index(agent.preference)]
    return {
            "shape": "rect",
            "color": color,
            "size": 50,
            }

model_params = {
        "width": {
            "type": "SliderInt",
            "value": 30,
            "label": "Width:",
            "min": 5,
            "max": 100,
            "step": 1,
            }
        }

page = JupyterViz(
        VotingModel,
        model_params,
        measures=["Votes"],
        name="Stratetic Voting Model",
        agent_portrayal=agent_portrayal,
        )
