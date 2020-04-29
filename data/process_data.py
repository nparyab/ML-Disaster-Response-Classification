import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    messages = pd.read_csv(messages_filepath)
    messages.head()
    categories = pd.read_csv(categories_filepath)
    print(categories.head())

    # merge datasets
    df = messages.merge(categories, how='outer', on=['id'])
    print(df.head())
    categories = df.categories.str.split(';', n=-1, expand=True)

    #df = imputing(categories,df)
    print ("Imputing categoty data with numerical values ... ")
    category_colnames = []
    for column in categories.columns:
        vals = categories[column].unique()
        category_colnames.append(str(vals[0]).split("-")[0])
    print(category_colnames)
    # rename the columns of `categories`
    categories.columns = category_colnames
   
    # ### 4. Convert category values to just numbers 0 or 1.
    # - Iterate through the category columns in df to keep only the last character of each string (the 1 or 0). For example, `related-0` becomes `0`, `related-1` becomes `1`. Convert the string to a numeric value.
    # - You can perform [normal string actions on Pandas Series](https://pandas.pydata.org/pandas-docs/stable/text.html#indexing-with-str), like indexing, by including `.str` after the Series. You may need to first convert the Series to be of type string, which you can do with `astype(str)`.

    for column in categories:
      # set each value to be the last character of the string
      categories[column] = categories[column].apply(lambda x: str(x).split("-")[1])
      # convert column from string to numeric
      categories[column] = categories[column].astype(int)

    categories.head()
    # ### Replace `categories` column in `df` with new category columns.
    # - Drop the categories column from the df dataframe since it is no longer needed.
    # - Concatenate df and categories data frames.
    df.drop(labels=["categories"], axis="columns", inplace=True)
    df.head() 
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df,categories], axis=1, sort=False)
    return df

#def imputing(categories,df):



"""
# ### Remove duplicates.
  # - Check how many duplicates are in this dataset.
  # - Drop the duplicates.
  # - Confirm duplicates were removed.
"""
def clean_data(df):
    #df = imputing(df)
    # check number of duplicates
    print("The total number of datapoints: ",len(df))
    print("Duplicated rows:", len(df[df.duplicated()]))

    # drop duplicates
    df = df.drop_duplicates()
    print("The total number of unique datapoints:", len(df))

    # check number of duplicates for double-check
    print("Duplicated rows:", len(df[df.duplicated()]))
    return df



def save_data(df, database_filename):
    engine = create_engine('sqlite:///'+ ("data/DisasterResponse"))
    df.to_sql('DResponseTable', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()