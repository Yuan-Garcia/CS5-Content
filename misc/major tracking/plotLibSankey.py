import cleaning
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

graduated = cleaning.graduated

# Extract unique nodes
nodes = list(set([item for sublist in graduated for item in sublist]))

# Create a dictionary to map nodes to unique integers
node_map = {node: i for i, node in enumerate(nodes)}

# Create lists to store source, target, and value for each flow
sources = [node_map[row[0]] for row in graduated]
targets = [node_map[row[3]] for row in graduated]
values = [1] * len(graduated)  # Assuming each flow has a value of 1

# Create the Sankey diagram
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[], title="Student Flow")
sankey = Sankey(ax=ax, unit=None)
sankey.add(flows=values, labels=nodes, orientations=[0]*len(nodes), color='blue')
sankey.finish()
plt.show()

