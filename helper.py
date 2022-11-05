import numpy as np
import streamlit


def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','City','NOC','Games','Year','Sport','Event','Medal'])
    flag=0
    if year == 'Overall' and country == 'Overall':
      temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
      flag=1
      temp_df = medal_df[medal_df['region']==country]
    if year != 'Overall' and country == 'Overall':
      temp_df = medal_df[medal_df['Year']==int(year)]
    if year != 'Overall' and country !='Overall':
      temp_df =  medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]
    if flag==1:
       x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
       x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=True).reset_index()

    x['total']=x['Gold']=x['Silver']=x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')
    return x
def medal_tallly(df):
    medal_tally = df.drop_duplicates(subset=['Team','City','NOC','Games','Year','Sport','Event','Medal'])
    medal_tally = medal_tallly.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold'] + medal_tally['Silver']+  medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['total']=medal_tally['total'].astype('int')

    return medal_tally

def country_Year_list(df):
    Year = df['Year'].unique().tolist()
    Year.sort()
    Year.insert(0,'Overall')
    Country = np.unique(df['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0,'Overall')
    return Year,Country
def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index':'Edition','Year':col},inplace=True)
    return nations_over_time
def most_successful(df,sport):
     temp_df=df.dropna(subset=['Medal'])
     if sport != 'Overall':
         temp_df = temp_df[temp_df['Sport']==sport]
     x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
     x.rename(columns={'index':'Name','Name_x':'Medal'},inplace=True)
     return x
def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df= new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df
def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt
def most_successful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['region']==country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medal'}, inplace=True)
    return x

def men_vs_women(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x:':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    return final
