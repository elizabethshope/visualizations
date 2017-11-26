# Imports
import pandas as pd

# Define data sources
### IF YOU ARE RUNNING THIS CODE, YOU WILL NEED TO UPDATE THE DIRECTORY PATH
### TO THE DIRECTORY WHERE YOU HAVE YOUR FILES
directory = '../../../Documents/portfolio/'

filenames = ['ratings_Amazon_Instant_Video.csv', 'ratings_Clothing_Shoes_and_Jewelry.csv',
             'ratings_Digital_Music.csv', 'ratings_Electronics.csv', 'ratings_Home_and_Kitchen.csv',
             'ratings_Video_Games.csv']

data_sources = [directory + filename for filename in filenames]

# Set names of categories for use in data frame
categories = ['Amazon Instant Video', 'Clothing Shoes and Jewelry', 'Digital Music', 'Electronics',
              'Home and Kitchen', 'Video Games']

# Define function to get absolute counts and fractions of each star review
def get_counts_fractions(file):
    df = pd.read_csv(file, header=None)
    df.columns = ['user', 'item', 'rating', 'timestamp']
    counts = df.rating.value_counts()
    counts_list = [counts[i] for i in range(1, 6)]
    fractions_list = [counts[i]/sum(counts) for i in range(1, 6)]
    return counts_list, fractions_list

# Get counts and fractions for each source & put into data frame
counts_df = pd.DataFrame()
counts_df['ratings'] = [1, 2, 3, 4, 5]

fractions_df = pd.DataFrame()
fractions_df['ratings'] = [1, 2, 3, 4, 5]

for j in range(len(filenames)):
    counts, fractions = get_counts_fractions(data_sources[j])
    counts_df[categories[j]] = counts
    fractions_df[categories[j]] = fractions

# Print count and fraction dataframes
print(counts_df)
print(fractions_df)

# Save the fraction dataframe to CSV
fractions_df.to_csv('Amazon_Reviews_Star_Fractions.csv', index=False)

