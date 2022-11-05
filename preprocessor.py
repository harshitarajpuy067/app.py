import pandas as pd

def preprocessor(df,region_df):
    #filltering for summer olympic
    df = df[df['Season'] == 'Summer']
    #merge with region df
    df = df.merge(region_df, on='NOC', how='left')
    #delete duplicate values
    df.drop_duplicates(inplace=True)
    #one not encoding medal
    df = pd.concat([df, pd.get_dummies(df['Medal'])],axis=1)
    return df