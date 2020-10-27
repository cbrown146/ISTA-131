'''
Author: Christopher D. Brown
Date: 10/24/19
Class: ISTA 131
Section Leader: Thomas Gregory Frauenfeld
Collaborators: Ben Henning

Description:
This program will read in a csv file removing the ',' and setting the index to 0.  
It will remove whitespace and capitalize each word in the rows.  The growth rate 
will be found by subtracting the death rate from the birthrate.  We will add
columns to the DataFrame 'Years to Extinction', 'Growth Rate'.  Later, we will 
sort the countries that are facing extinction.  The sorting will go from the countries 
that face imminent extinctino to the countries that have some time.  

Finally, all of this information will be framed nicely and presented.  
'''


import pandas as pd 
import numpy as np 

def csv_to_dataframe(csv): 

    df = pd.read_csv('countries_of_the_world.csv', decimal=',', index_col= 0)  

    
    return df

def format_df(df): 
    """
    This function takes a dataframe and strips the whitespace from the rows. Afterwhich 
    it adds a column to the dataframe.  
    """
     
    df.index = df.index.str.strip()

    #strip Region
    df['Region'] = df['Region'].str.strip()
    df['Region'] = df['Region'].str.title()

    


    
    

def growth_rate(df): 
    """
    The growth_rate function subtracts the Birthrate column from the Deathrate column. 
    NOT ALL AT ONCE.  The growth_rate is saved into a new column called 'Growth Rate'. 
      
    """ 
    
    #Add new column labeled 'Growth Rate' to the frame.  
    growth_rate = df.loc[:,'Birthrate'] - df.loc[:,'Deathrate']
    
    df['Growth Rate'] = growth_rate

    


    
def dod(p, r):
    """
    Helper function provided by D2l.  his function takes an initial population and a growth rate (which must be negative – why?) in 1000's 
    of individuals per year and returns the number of years it will take for the population of the country to go extinct if the growth rate
    doesn't change.  We consider the population extinct if it is down to no more than two individuals, but this stretches out the time 
    considerably because of the way the math of exponential decay works. 1,000 or 10,000 individuals would probably be more reasonable 
    definition of extinct.
    """
    num_yrs = 0     
    while p > 2:         
        p = p + p * r / 1000          
        num_yrs += 1     
    return num_yrs 

def years_to_extinction(df):
    """
For this function,  we add a column to the dataframe.  It's called 'Years to Extinction'
We will set empty values to the column.  We will find the populations with the lowest growth rates and
save them to 'Years to Extinction'.  This will allow us to see how much longer a country has in years
before they die off due to low population and growth rate.  

    """ 
    df['Years to Extinction'] = np.nan
    
    for row in df.index:
        if df.loc[row,'Growth Rate'] < 0: 
            df.loc[row, 'Years to Extinction'] = dod(df.loc[row,'Population'], df.loc[row,'Growth Rate'])
    
def dying_countries(df): 
    """
This function returns a Series of the 'Years to Extinction'.  The NaN values are
dropped and the countries that will die first appear first to last.  
    """  
    return df['Years to Extinction'].dropna().sort_values()

#def main('countries_of_the_world.csv'):
#def main(countries_of_the_world.csv):
#def main(df):
def main():
    """
This function returns a Series of the 'Years to Extinction'.  The NaN values are
dropped and the countries that will die first appear first to last.  
    """ 
    df = csv_to_dataframe('countries_of_the_world.csv')
    format_df(df) 
    growth_rate(df)
    years_to_extinction(df)
    dc = dying_countries(df)
     
    for i in range(0,5):
        
        print(dc.index[i]+ ":", dc.iloc[i] , "Years to Extinction")

   
