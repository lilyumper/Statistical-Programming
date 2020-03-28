import numpy as np
import pandas as pd
import matplotlib as ml

# got to read the data and set it up as recommended in the pdf as well as using SBL to true
# this will skip blank lines within our data
data_df = pd.read_csv('ss13hil.csv', usecols=['HHT', 'HHL', 'HINCP', 'WGTP', 'ACCESS'], skip_blank_lines=True)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# Next we have to map the categores for accss and make it into the first table
# we will make each category into an set
def first_table(data_df):
    # We will set HHT to a set and name the rows
    HHT = {
        1: 'Married couple household',
        2: 'Other family household: Male householder, no wife present',
        3: 'Other family household: Female householder, no husband present',
        4: 'Nonfamily household: Male householder:Living alone',
        5: 'Nonfamily household: Male householder: Not living alone',
        6: 'Nonfamily household: Female householder:Living alone',
        7: 'Nonfamily household: Female householder: Not living alone'
    }
    # Then we will map it out
    data_df['HHT'] = data_df['HHT'].map(HHT)

    # we then will use a pivot table to get our columnns and using aggfunc to get our
    # mean, std, min, max, and count
    table_one = pd.pivot_table(data_df, values=['HINCP'], index=['HHT'], aggfunc=('mean', 'std', 'min', 'max', 'count'))

    # Next we have to to set the index name of table one
    # we will also then set the columns and use drop level
    # this means if a multi index has only 2 levels which we have here the results will be of index type not multi index
    table_one.index.name = 'HHT - Household/family type'
    table_one.columns = table_one.columns.droplevel()

    # we will then get our min and max columns added and setting the type to int we will then print
    table_one['min'] = table_one['min'].astype(int)
    table_one['max'] = table_one['max'].astype(int)
    print("Table #1 - Descriptive Statistics of HINCP, grouped by HHT")
    print(table_one[['mean', 'std', 'count', 'min', 'max']].sort_values(by='mean', ascending=False))
    print('\n')


def second_table(data_df):
    # we will do the same as we did above for table 2 now we will set the access and HHL
    # access will be our columns now will be our access set
    access = {1: 'Yes, w/ Subscr.', 2: 'Yes, wo/ Subscr.', 3: 'No'}
    HHL = {
        1: 'English only',
        2: 'Spanish',
        3: 'Other Indo-European languages',
        4: 'Asian and Pacific Islan languages',
        5: 'Other'}
    # now we have to map them out  using by the rows
    data_df.ACCESS = data_df.ACCESS.map(access)
    data_df['HHL'] = data_df['HHL'].map(HHL)

    # we will then set our table to a data frame and get our data from thos columns
    table_two = data_df[['HHL', 'ACCESS', 'WGTP']].dropna()

    # we then will calucalte the sum from WGTP as and then we put it back into the wgtp column
    wgt_total = table_two['WGTP'].sum()
    table_two['WGTP'] = 100 * (table_two['WGTP'] / wgt_total)

    # we will again do the same thing for this table as we did in table 1
    table2 = pd.pivot_table(table_two, values=['WGTP'], columns=['ACCESS'], index=['HHL'], margins=True, aggfunc=sum)

    # now we are going to print the columns in the order as well as sorting the values.
    # still cannot figure out how to format to percentages
    print("Table #2 - HHL vs ACCESS - Frequency Table")
    print(table2.WGTP[['Yes, w/ Subscr.', 'Yes, wo/ Subscr.', 'No', 'All']].sort_values(by='Yes, w/ Subscr.',
                                                                                        ascending=False))
    print('\n')


# last and least we move to the last table

def table_3(data_df):
    # we will utilize the qcut as recommened during lecture ###THANK YOU
    # q cut will help create equal size buckets of a variable
    data_df['HINCP_QUANTILES'] = pd.qcut(data_df['HINCP'], 3, labels=["low", "medium", "high"])

    # we wil do the same as the previous 2
    table_three = pd.pivot_table(data_df, index=['HINCP_QUANTILES'],
                                 aggfunc=({'HINCP': ('min', 'max', 'mean'), 'WGTP': sum}))

    # again same as the first table we are table one we are to drop a level and rename some columns
    table_three.columns = table_three.columns.droplevel()
    table_three.rename(columns={'sum': 'household_count'}, inplace=True)
    table_three.index.name = 'HINCP'
    table_three['min'] = table_three['min'].astype(int)
    table_three['max'] = table_three['max'].astype(int)

    # now we print everything in order
    print("Table #3 - Quantile Analysis of HINCP - Household Income (Past 12 Months) ")
    print(table_three[['min', 'max', 'mean', 'household_count']])


def runIt(data_df):
    print("DATA-51100")
    print("Thomas Garcia")
    print("Assignment #7")
    print("\n")
    first_table(data_df)
    second_table(data_df)
    table_3(data_df)


runIt(data_df)
