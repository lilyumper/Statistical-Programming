import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

print("CPSC-51100, Spring 2020")
print("NAME:  Alexander Del Valle")
print("NAME:  Thomas Garcia")
print("NAME:  Alison Werr")
print("PROGRAMMING ASSIGNMENT #6")
print(" ")
#
# Read the 2013 ACS 1-year PUMS data for Illinois Housing Unit Records into a dataframe
#
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)
ss13hil_df = pd.read_csv('ss13hil.csv')
#
# Create the figure to hold the four subplots
#
fig = plt.figure()
fig.set_size_inches(20, 14)
#
# Create the four subplots.  All Subplots are 2X2.
# First two numbers in the subplot function show the subplot shoult be 2X2 where the last number is the figure placement on the plot.
#
ax1 = fig.add_subplot(2,2,1) # will hold the pie chart in upper left corner
ax2 = fig.add_subplot(2,2,2) # will hold the histogram in upper right corner
ax3 = fig.add_subplot(2,2,3) # will hold the bar chart in lower left corner
ax4 = fig.add_subplot(2,2,4) # will hold the scatter plot in lower right corner
#
# Create the pie chart
#
# Initialize chart specific variables such as colors, lables, and number of data entries.
pie_chart_data   = [0, 0, 0, 0, 0]  #Create an array of five numbers since there are five different language categories
laguage_categories = ['English Only', 'Spanish', 'Other Indo-European', 'Asian and Pacific Island Languages', 'Other']
# The following contain the color codes for the pie chart:
#                   blue     orange     green       red       purple
pie_chart_colors = ['#0088cc', 'orange', '#2fb62f', '#e63900', 'purple']



#
# Total Number of Entries for the pie chart
# I basically want to take the total number of non-null rows to use as the denominator for the percentages calculations
#
chart_entries = len(ss13hil_df['HHL'].dropna().index)
#
# Calculate Percentage for languages spoken.  This will determine how big of a slice of the pie each language will occupy.
# Loop has to start at range 1 to 6 since that is how each language is denoted in the dataset.  Ex: english=1, spanish=2, etc.
for i in range(1, 6):
    pie_chart_data[i - 1] = (ss13hil_df['HHL'].value_counts()[i] / chart_entries) * 100

# Build the pie chart so that it conforms to assignment instructions
patches, text = ax1.pie(pie_chart_data, startangle = 242, colors = pie_chart_colors,)
ax1.set_title('Household Languages', fontsize = 20)
ax1.set_ylabel("HHL", fontsize = 12)
ax1.legend(patches, laguage_categories, loc = "upper left", prop = {'size' : 14})
ax1.axis('equal')



#
# Create the histogram
#
#Histogram of HINCP (household income) with KDE plot superimposed.
histogram_chart_data = ss13hil_df['HINCP'].dropna()
#
# Show kernal density estimation(KDE).  Will be using the import from scipy to calculate.
#
KDE_line = stats.gaussian_kde(histogram_chart_data)
KDE_linespacing = np.logspace(1, 7)
# Build Histograph so that it conforms to assignment instructions.
logspace = np.logspace(1,7,num=100,base=10.0)
ax2.hist(histogram_chart_data,bins=logspace,facecolor='g',alpha=0.5,histtype='bar', normed=True)
ax2.set_title('Distribution of Household Income',fontsize=20)
ax2.set_xlabel('Household Income($)- Log Scaled',fontsize=14)
ax2.set_ylabel('Density',fontsize=14)
ax2.set_xscale("log")
# Superimpose KDE line on the graph
ax2.plot(KDE_linespacing, KDE_line(KDE_linespacing), color = 'black', linestyle = '--', linewidth = 2)


#
# Create the bar graph
#
# Create list/array for the seven entries on the bar graph as well as the lables.
bar_graph_data = [0, 0, 0, 0, 0, 0, 0]
bar_graph_labels = ['0', '1', '2', '3', '4', '5', '6']

# As per directions, I will use the WGTP value to count how many households are
# represented by each household record and divide the sum by 1000
for i in range(0, 7):
    temp1_df = ss13hil_df[ss13hil_df['VEH'] == i]
    bar_graph_data[i] = temp1_df['WGTP'].dropna().sum() / 1000


# Build bar graph so that it conforms to assignment instructions
ax3.bar(bar_graph_labels, bar_graph_data, align = 'center', color = 'red')
ax3.set_title('Vehicles Available in Households', fontsize = 20)
ax3.set_xlabel('# of Vehicles', fontsize = 14)
ax3.set_ylabel('Thousands of Households', fontsize = 14)
ax3.tick_params(axis = 'both', labelsize = 10)
#plt.yticks(np.arange(0, 1750, 250))


#
# Create the scatter plot
#
taxp_data = ss13hil_df['TAXP']
#
# Create a dictionary and populate it with taxp info
# Note: This dictionary seeks to recreate the PUMS DATA PDF Chart list on page 15 of the PDF
#
taxp_ranges = {}
taxp_ranges[1] = np.NaN  #First value is always null.
taxp_ranges[2] = 1       #The start of the taxes will begin at $1
taxp_ranges[63]=5500     #Sets the value when tax bracket data starts increasing by 500 (this occurs inbetween $5000 and $6000 dollars)
iterator = 50
# For loop which increments by 50 until it reaches $1000
for key in range (3,23):
    taxp_ranges[key]=iterator
    iterator += 50
# For loop which increments the following units by 100 after it reaches $1000 until it hits $5000
for key in range (23,63):
    taxp_ranges[key] = iterator+50
    iterator += 100
iterator = iterator - 50
# For loop which increments the following elements by 1000 after it reaches $6000 until it hits $10000 (Max Coded Value)
for key in range (64,69):
    taxp_ranges[key] = iterator+1000
    iterator += 1000
#
# Convert the taxp code to a dollar amount.  These numbers will be used as points in the scatter plot.
#
tax_dollar_amounts = []
for i in taxp_data:
    if i in taxp_ranges:
        tax_dollar_amounts.append(taxp_ranges[i])
    else:
        tax_dollar_amounts.append(np.NaN)
#
# Read in the VALP data and set graph limits as per assignment instructions
#
valp_data = ss13hil_df['VALP']
ax4.set_ylim([0, 11000])
ax4.set_xlim([0, 1200000])
#
# Build bar graph so that it conforms to assignment instructions
#
scatter_image = ax4.scatter(valp_data,tax_dollar_amounts, s=ss13hil_df['WGTP'], c=ss13hil_df['MRGP'],cmap='seismic',alpha=0.20,marker = 'o')
ax4.set_title('Property Taxes vs Property Values',fontsize=20)
ax4.set_ylabel('Taxes($)',fontsize=14)
ax4.set_xlabel('Property Value($)',fontsize=14)
ax4.tick_params(axis='both', which='major', labelsize=10)
#
# Create and add the color bar
#
cbar = fig.colorbar(scatter_image, ax=ax4)
cbar.ax.tick_params(labelsize=10)
cbar.set_label('First Mortgage Payment (Monthly $)',fontsize=14)

#
#save the figure
#
plt.savefig('pums.png')
#
# Get the figure to display
#
plt.show()