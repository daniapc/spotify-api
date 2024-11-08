import pandas as pd
import os
import random

def find(array, artist):
    i = 0
    for item in array:
        if (item[1] == artist):
            return i
        i += 1
        
    return -1


df = pd.read_csv(os.getcwd() + '/src/data/tracks.csv')

artists = df['artist'].values

artists = list(set(artists))

df_values = list(df.values)
random.shuffle(df_values)

result = []

while (len (df_values) != 0):
    artists_copy = artists.copy()
    random.shuffle(artists_copy)
    for artist in artists_copy:
        index = find(df_values, artist)
        if index != -1:
            result.append([
                df_values[index][0],
                df_values[index][1],
                df_values[index][2]
            ]
                )
            df_values.pop(index)

for r in result:
    print(r)
