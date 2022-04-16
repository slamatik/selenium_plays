import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_csv('/Users/slamatik/Desktop/protein_shake.csv', skiprows=1)
df.columns = ['month', 'googles']
df = df[df.month > '2012']
df.month = pd.to_datetime(df.month)
dfmt = mdates.DateFormatter('%Y-%b')

fig, ax = plt.subplots(figsize=(16, 12))

ax.plot(df.month, df.googles)
ax.xaxis.set_major_formatter(dfmt)
# plt.grid()
ax.set_title = 'kek'
ax.set_xlabel = 'test'
ax.set_facecolor('black')
plt.show()