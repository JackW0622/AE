import pandas as pd
df = pd.read_csv('test 2.csv', header=None)
df.columns = df.iloc[0]    # 把首行当列名
df = df[1:].reset_index(drop=True)
df = df.dropna(axis = 1, how='all')
df.columns = df.columns.map(str)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df[['UKR219130', '11-Apr-25', 'Hlushchenkove', '49.2125', '37.7815', '0']]
df.columns = ['EventID', 'Date', 'Location', 'latitude', 'longitude', 'casualties']
df.to_csv('cleaned_data.csv', index=False)