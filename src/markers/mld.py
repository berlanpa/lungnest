import pandas as pd
import numpy as np
from bigtree import *
import SimpleITK as sitk
import hashlib
from scipy.stats import kurtosis, skew, skewnorm

from config.path import out
from config.dict import threshold

# define values to extract
df = pd.read_csv(out + "\\master.csv")
df = df.loc[df['Priority'] == 1]
df = df[["Hash","Patient", "Date", "Session", "Scan", "Type", "Mean"]]
# background check
df = df.sort_values(['Patient', 'Date'], ascending=[True, True])

# define output dataframe
columns = ['Patient', 'Date', 'E/I', 'INSPI', 'In.Loc.', 'In.Mean', 'EXPI', 'Ex.Loc.', 'Ex.Mean']
df2 = np.unique(df[['Patient','Date']].values.astype(str), axis=0)
df2 = np.c_[ df2, np.zeros(len(df2)*(len(columns) - 2)).reshape(len(df2),-1)]

# populate dataframe
count = 0
for i in range(len(df)):
    row = df.iloc[i]
    if i == 0:
        df2[0,6], df2[0,7], df2[0,8] = row["Hash"], "-".join([row["Session"],row["Scan"]]), row["Mean"]
    elif row["Date"] != df.iloc[i - 1]["Date"]:
        count += 1
    if row["Type"] == 'EXPI': df2[count,6], df2[count,7], df2[count,8] = row["Hash"], "-".join([row["Session"],row["Scan"]]), row["Mean"]
    elif row["Type"] == 'INSPI': df2[count,3], df2[count,4], df2[count,5] = row["Hash"], "-".join([row["Session"],row["Scan"]]), row["Mean"]
df2 = pd.DataFrame(df2, columns = columns)


# calculate E/I
for i in range(len(df2)):
    row = df2.iloc[i]
    if row['In.Mean'] != 0 and row['Ex.Mean'] != 0:
        df2.at[i,'E/I'] = float(row['Ex.Mean']) / float(row['In.Mean'])

# output dataframe
df2.to_csv(out + "\\mld.csv", index=False)




