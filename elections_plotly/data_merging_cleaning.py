# Imports
import pandas as pd
import us

# Read in data
# These results are official and came from https://transition.fec.gov/pubrec/fe2012/federalelections2012.shtml
# I have slightly cleaned them to make them easy to read in
election_results = pd.read_csv('election_results.csv', sep='\t')

# Change "D.C." to District of Columbia so that it can be found by the state finder
election_results.iloc[8, 0] = 'District of Columbia'

# Add in Clinton v Trump results
# These are unofficial taken from https://docs.google.com/spreadsheets/d/1D-edaVHTnZNhVU840EPUhz3Cgd7m39Urx7HM8Pq6Pus/edit#gid=29622862
# This source got them from Dave Leip's Atlas https://uselectionatlas.org/
election_results['CLINTON2016'] = [34.4,  36.6,  44.6,  33.7,  61.5,  48.2,  54.6,  53.1,  90.9,
                                   47.4,  45.3,  62.2,  27.5,  55.2,  37.5,  41.7,  35.7,  32.7,
                                   38.4,  47.8,  60.3,  60.0,  47.0,  46.4,  40.1,  37.9,  35.4,
                                   33.7,  47.9,  46.8,  55.0,  48.3,  59.0,  46.2,  27.2,  43.2,
                                   28.9,  50.1,  47.5,  54.4,  40.7,  31.7,  34.7,  43.2,  27.2,
                                   56.7,  49.8,  52.5,  26.2,  46.5,  21.9]


election_results['TRUMP2016'] = [62.1,  51.3,  48.1,  60.6,  31.5,  43.3,  40.9,  41.7,   4.1,
                                 48.6,  50.4,  30.0,  59.2,  38.4,  56.5,  51.1,  56.2,  62.5,
                                 58.1,  44.9,  33.9,  32.8,  47.3,  44.9,  57.9,  56.4,  55.6,
                                 58.7,  45.5,  46.5,  41.0,  40.0,  36.5,  49.8,  63.0,  51.3,
                                 65.3,  39.1,  48.2,  38.9,  54.9,  61.5,  60.7,  52.2,  45.1,
                                 30.3,  44.4,  36.8,  67.9,  47.2,  68.2]


# Add in a state code
election_results['CODE'] = [us.states.lookup(state).abbr for state in election_results['STATE']]

# Get rid of the % sign in some of the rows
for col in election_results.columns[1:7]:
    election_results[col] = [entry[:-1] for entry in election_results[col]]

# Cast all columns as strings
for col in election_results.columns:
    election_results[col] = election_results[col].astype(str)

# Turn into a long data frame
election_results_long = pd.DataFrame()
election_results_long['state'] = list(election_results['STATE']) * 6
election_results_long['code'] = list(election_results['CODE']) * 6
election_results_long['year'] = [2016] * 51 + [2012] * 51 + [2008] * 51 + [2004] * 51 + [2000] * 51 + [1996] * 51
election_results_long['dem'] = list(election_results['CLINTON2016']) + list(election_results['OBAMA2012']) + \
                               list(election_results['OBAMA2008']) + list(election_results['KERRY2004']) + \
                               list(election_results['GORE2000']) + list(election_results['CLINTON1996'])

election_results_long['rep'] = list(election_results['TRUMP2016']) + list(election_results['ROMNEY2012']) + \
                               list(election_results['MCCAIN2008']) + list(election_results['BUSH2004']) + \
                               list(election_results['BUSH2000']) + list(election_results['BUSH1996'])

# Save long data frame to csv
election_results_long.to_csv('election_results_long.csv', index=False)
