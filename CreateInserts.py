import pandas as pd

df = pd.read_csv('posts.csv')
cols = df.columns.tolist()

f = open('inserts.txt', 'w')

for i in range(len(df)):
    insert = 'INSERT INTO NAP.article ('
    for j, col in enumerate(cols):
        insert += col
        if j < len(cols) - 1:
            insert += ', '
    
    insert += ') VALUES ('

    for j, col in enumerate(cols):
        datum = df.iloc[i][col]
        if type(datum) == str:
            datum = datum.replace("'", "\\'").replace('"', '\\"')
            datum = "'" + datum + "'"
        else:
            datum = str(datum)
            datum = datum.replace("'", "\\'").replace('"', '\\"')

        insert += datum
        
        if j < len(cols) - 1:
            insert += ', '

    insert = insert.replace('\u200b', '')

    insert += ');'
    f.write(f'{insert}\n')

f.close()
