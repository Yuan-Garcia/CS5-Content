import pandas as pd

###############################
# major key:
# HEGR: Engineering
# HBIO: Biology
# HMAT: Mathematics
# HPHY: Physics
# HCHE: Chemistry
# HCSI: Computer Science
# HCSM: Computer Science + Math
# HMCB: Math + Computer Science + Biology ???
# HMAB: Math + Biology
# HCHB: Chemistry + Biology
# HMPH: Math + Physics
# HUND: Undeclared
# HIPS: Independent Study
# HOFF: Off Campus

df = pd.read_csv('og_graduated_student_data.csv')
###############################


def count_major(year):
    if year: 
        declared_count = df[(df['Declared Major'].str.strip() == declared_major) & (df['Year'] == year)]
        graduated_count = df[(df['Graduated Major'].str.strip() == graduated_major) & (df['Year'] == year)]
    else:
        declared_count = df[df['Declared Major'].str.strip() == declared_major]
        graduated_count = df[df['Graduated Major'].str.strip() == graduated_major]

    declared_count = declared_count.shape[0]
    graduated_count = graduated_count.shape[0]

    return declared_count, graduated_count


def major_switches_from_declared(declared_major, year):
    switches = {}
    for index, row in df.iterrows():
        if year:
            if row['Declared Major'].strip() == declared_major and row['Year'] == year:
                end_major = row['Graduated Major']
                if end_major in switches:
                    switches[end_major] += 1
                else:
                    switches[end_major] = 1
        else:
            if row['Declared Major'].strip() == declared_major:
                end_major = row['Graduated Major']
                if end_major in switches:
                    switches[end_major] += 1
                else:
                    switches[end_major] = 1
    
    results = []
    for major, counts in switches.items():
        results.append(f"{declared_major} -> {major}: {counts}")

    return "\n".join(results)

def major_switches_to_graduated(graduated_major, year):
    switches = {}
    for index, row in df.iterrows():
        if year:
            if row['Graduated Major'].strip() == graduated_major and row['Year'] == year:
                start_major = row['Declared Major']
                if start_major in switches:
                    switches[start_major] += 1
                else:
                    switches[start_major] = 1
        else:
            if row['Graduated Major'].strip() == graduated_major:
                start_major = row['Declared Major']
                if start_major in switches:
                    switches[start_major] += 1
                else:
                    switches[start_major] = 1
    
    results = []
    for major, counts in switches.items():
        results.append(f"{major} -> {graduated_major}: {counts}")

    return "\n".join(results)

def num_grads():
    majors = {}
    for index, row in df.iterrows():
        major = row['Graduated Major']
        if major in majors:
            majors[major] += 1
        else:
            majors[major] = 1
    
    results = []
    for major, counts in majors.items():
        results.append(f"{major}: {counts}")
    return "\n".join(results)



############################################
# print statements to show data

# edit as needed
declared_major = "HBIO"
graduated_major = "HBIO"
year = None

############################################

declared_count, graduated_count = count_major(year)
if year is None:
    print(f"The total number of students from 2007-2019 who declared {declared_major}: {declared_count}")
    print(f"The total number of students from 2007-2019 who graduated with {graduated_major}: {graduated_count}")
else:
    print(f"Number of people that declared HMAT in {year}:", declared_count)
    print(f"Number of people that graduated with HMAT in {year}:", graduated_count)   


print("\n")
if year is None:
    print(f"The number of major switches from {declared_major} are:")
else:
    print(f"The number of major switches from {declared_major} in {year} are:")
declared_switches = major_switches_from_declared(declared_major, year)
print(declared_switches)

print("\n")
if year is None:
    print(f"The number of major switches to {graduated_major} are:")
else:
    print(f"The number of major switches to {graduated_major} in {year} are:")
graduated_switches = major_switches_to_graduated(graduated_major, year)
print(graduated_switches)

print("\n")
print("The number of graduates in each major are:")
grads = num_grads()
print(grads)