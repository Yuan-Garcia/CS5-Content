import DataRequest_Dictionary_int_act_mapped_for_florence
import plotly.graph_objects as go

# clean up data to include students that recieved or will recieve a degree
all_Data = DataRequest_Dictionary_int_act_mapped_for_florence.int_act
graduated = {}
for x in all_Data:
    if "Graduated" or "Pending Commencement" in x[2]:
        graduated[tuple(x)] = x
#print(graduated)

# getting each unique major
starting_major = []
ending_major = []
for x in graduated:
    starting_major.append(x[0])
    ending_major.append(x[3])
starting_major = list(set(starting_major))
ending_major = list(set(ending_major))

# create a sankey diagram for graduated students
all_majors = list(set(starting_major + ending_major))
major_dict = {major: idx for idx, major in enumerate(all_majors)}
sources = []
targets = []
values = []

for key, value in graduated.items():
    sources.append(major_dict[value[0]])
    targets.append(major_dict[value[3]])
    values.append(1)

figure = go.Figure(data=[go.Sankey(
    node=dict(
        pad = 15,
        thickness = 20,
        line = dict(color="black", width=0.5),
        label = all_majors
    ),
    link = dict(
        source = sources,
        target = targets,
        value = values
    )
)])

figure.update_layout(title_text="Major switches of students from 2007-2019", font_size=14, width=800, height=600)
figure.show()


