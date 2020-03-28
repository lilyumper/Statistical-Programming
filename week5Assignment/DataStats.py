import pandas as pd
import numpy as py
import re

# First we have to read and get the data wanted our data
school_info = pd.read_csv('cps.csv')
selected_info = school_info[
    ['School_ID', 'Short_Name', 'Is_High_School', 'Zip', 'Student_Count_Total',
     'College_Enrollment_Rate_School',
     'Grades_Offered_All',
     'School_Hours']].sort_index()


# replacing the missing numerical values for the mean of that column

def replace_NAN(selected_info):
    for x in selected_info.select_dtypes(['float64', 'int64']).columns:
        # fillna will grab all the NAN values
        selected_info[x].fillna(selected_info[x].mean(), inplace=True)
        return selected_info


# lets find the mean and STD of college enrollment for highSchools

def meanSTD_CollegeEnrollmentCount_HS(selected_info):
    mean = selected_info.groupby('Is_High_School')['College_Enrollment_Rate_School'].mean()
    std = selected_info.groupby('Is_High_School')['College_Enrollment_Rate_School'].std()

    # selected the first second part of the mean and std and rounding it to the hundreth
    print('College Enrollment Rate for High Schools = ', mean[1].round(2), ' (std = ', std[1].round(2), ')', "\n")


def meanSTD_StudentCount_nonHS(selected_info):
    mean = selected_info.groupby('Is_High_School')['Student_Count_Total'].mean()
    std = selected_info.groupby('Is_High_School')['Student_Count_Total'].std()

    print('Total Student Count for Non-High Schools = ', mean[1].round(2), ' (std = ', std[1].round(2), ')', "\n")


# lets not look into getting the grades settled. WE can do this using the apply command along with the interation lamda

def grades(selected_info):
    # again now transforming the columns to iterate and apply the new name at a point as well as replacing the , and empty spaces
    selected_info['lowest_grade'] = selected_info.apply(lambda grade: grade['Grades_Offered_All'][0:2], 1).str.replace(
        ",", '')
    selected_info['highest_grade'] = selected_info.apply(lambda grade: grade['Grades_Offered_All'][-2:], 1).str.replace(
        ",", '')
    return selected_info


# next we deal with time and thanks for this part

def start_time(x):
    if str(x[0]) == 'nan':
        return 0
    else:
        return int(re.findall(r'[1-9]', x[0])[0])


time = selected_info[['School_Hours']].apply(start_time, axis=1)
selected_info = selected_info.assign(Starting_Hour = time)

# distrubutution of starting hours for all schools

def distrubution_start_time(selected_info):
    seven_am_start = []
    eight_am_start = []
    nine_am_start = []
    for time in selected_info['Starting_Hour']:
        if time == 7:
            seven_am_start.append(time)
        if time == 8:
            eight_am_start.append(time)
        if time == 9:
            nine_am_start.append(time)

    print('Distribution of Starting Hours should be:', '\n')
    print('7am: ', len(seven_am_start), '\n')
    print( '8am: ', len(eight_am_start), '\n')
    print( '9am: ', len(nine_am_start),  '\n')



def run_por_Favor(selected_info):
    print('DATA-51100')
    print('Thomas Garcia')
    print('Assignment 5')
    grades(selected_info)
    replace_NAN(selected_info)
    # dropping unwanted columns
    selected_info = selected_info.drop(['Grades_Offered_All', 'School_Hours'], axis = 1)
    print(selected_info.iloc[0:10, 0:9])
    meanSTD_CollegeEnrollmentCount_HS(selected_info)
    meanSTD_StudentCount_nonHS(selected_info)
    distrubution_start_time(selected_info)

run_por_Favor(selected_info)
