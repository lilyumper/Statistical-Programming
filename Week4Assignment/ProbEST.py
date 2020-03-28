import pandas as pd


# making the reading/selecting of data a function
# we are going to call this first to get our info in later functions


def getting_Data_Info():
    car_info = pd.read_csv('cars.csv')
    cars_picked = car_info[['make', 'aspiration']]
    return cars_picked


''' 
We have to find out how many cars were selected as well as what is the probability of the cars being selected
First we are going to put all into a function
Let's start with make probability
first we find the car make counts
so we use our cars picked as a parameter then we have to first find the make count that was selected
then we are going to sort the values of the count alphabetically and we do that combined with value counts
this shows the data in descending order
'''


def make_prob(cars_picked):
    car_make_count = cars_picked.make.value_counts().sort_index()
    selected_car_count = cars_picked['make'].count()
    car_make_prob = (car_make_count / selected_car_count * 100).round(decimals=2)
    make_prob_dataframe = pd.DataFrame({'car_make_name': cars_picked['make'].unique(), 'car_make_prob': car_make_prob})
    print_those_numbers = lambda car: print('Prob of Car (Make=' + car.car_make_name + ') = ', car.car_make_prob, '%')
    make_prob_dataframe.apply(print_those_numbers, axis=1)


'''
we need to find the number of counts selected
now we have to make the prob count and round it to two decimals
next we have to print the  information
however we have to convert that series of data into a dataframe
this will make to 
we name the columns as well and make that data returned unique
next we have to make this an anon function and we do that with lambda this again helps us shorten our code
then we apply a function along the axis in this case we want the axis 1. we do it with the .apply helper
apply takes int the function and in our case it is ptn and it takes an axis
'''

'''
next we have to find the conditional prob which is P(x | y)
as explained during lecture we have to utilize the crosstab helper that pandas offers
this computes a frequencey table
'''


def conditional_prob(cars_picked):
    cross_tab = pd.crosstab(index=cars_picked.make, columns=cars_picked.aspiration)
    cross_tab = pd.DataFrame(cross_tab)
    print(cross_tab)


# and last we make a full program run
# def print_it_all(cars_picked):
#     df1 = make_prob(cars_picked)
#     df2 = conditional_prob(cars_picked)
#     print(df1 + df2)


# def merge_it(cars_picked):
#     first = make_prob(cars_picked)
#     second = conditional_prob(cars_picked)
#     merge_em = pd.merge(left=first, right=second, left_on='make', right_on='make')


def run_this_por_favor():
    print("DATA 51100")
    print("Thomas Garcia")
    print("Assignment # 4\n")
    cars_picked = getting_Data_Info()
    conditional_prob(cars_picked)
    print('\n')
    make_prob(cars_picked)


run_this_por_favor()
