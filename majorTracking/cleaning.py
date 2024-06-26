import DataRequest_Dictionary_int_act_mapped_for_florence
import pandas as pd


# clean to only include Graduated and Pending Commencement students
all_Data = DataRequest_Dictionary_int_act_mapped_for_florence.int_act
graduated_students = [x for x in all_Data if x[2].strip() in ['Graduated', 'Pending Commencement']]
df_students = pd.DataFrame(graduated_students, columns=['Declared Major', 'Year', 'Status', 'Graduated Major'])
df_students.to_csv('graduated_student_data.csv', index=False)

# change all off campus majors to HOFF
all_majors = pd.read_csv('graduated_student_data.csv')
for index, row in all_majors.iterrows():
    if not row['Graduated Major'].startswith("H"):
        all_majors.at[index, 'Graduated Major'] = "HOFF"
all_majors.to_csv('graduated_student_data.csv', index=False)



# testing stuff

L = pd.read_csv('graduated_student_data.csv')
# L = pd.read_csv('og_graduated_student_data.csv')
count = 0
for index, row in L.iterrows():
    if row['Graduated Major'].strip() == 'HMAT':
        count += 1

not_grad = [x for x in all_Data if x[2].strip() not in ['Graduated', 'Pending Commencement']]
print(len(not_grad))

