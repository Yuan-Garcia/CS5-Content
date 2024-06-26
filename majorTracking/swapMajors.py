import pandas as pd

# major swaps, 
SWPR = { 'HEGR': 'HBIO',   # original : mapped 
         'HBIO': 'HMAT',
         'HMAT': 'HPHY',
         'HPHY': 'HCHE',
         'HCHE': 'HCSI',
         'HCSI': 'HCSM',
         'HCSM': 'HEGR',
         'HMCB': 'HMCB',
         'HMAB': 'HMAB',
         'HUND': 'HUND',
         'HIPS': 'HIPS',
         'HOFF': 'HOFF',
         'HCHB': 'HCHB',
         'HMPH': 'HMPH',}


df = pd.read_csv('graduated_student_data.csv')
df['Graduated Major'] = df['Graduated Major'].map(SWPR).fillna(df['Graduated Major'])
df['Declared Major'] = df['Declared Major'].map(SWPR).fillna(df['Declared Major'])
df.to_csv('og_graduated_student_data.csv', index=False)
print("Data has been cleaned and saved to 'og_graduated_student_data.csv'")