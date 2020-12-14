#Anthony Guzman             CIS2348                 #1503239

#--Importing the required libraries-------

# import pandas as pd so we can leverage the pd function to read the csv files
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import datetime

#-----------Import the data into their dataframes-------


# Used panda read csv() function to read the data from each file
# load the data from each of the  files into corresponding  DataFrames

#SInce the csv files don't have any headers, we had to define the headers
#Defined headers in names
ManufacturerList=pd.read_csv('ManufacturerList.csv ' ,header=None,names=["ID","Manufacturer Name","Item Type","Damaged"])

PriceList=pd.read_csv('PriceList.csv',header=None,names=["ID","Price"])

ServiceDatesList=pd.read_csv('ServiceDatesList.csv',header=None,names=["ID","Service Date"])



#------------  Part 1  ------------------------------
#--------------Processed Inventory Reports-----------


#------------Part a (Full Inventory)-----------------

#Merge the first two files together on base of ID
dataAll=pd.merge(ManufacturerList,PriceList,how='inner',left_on='ID',right_on='ID')

#Merge the previous file and last file together
FullInventory=pd.merge(dataAll,ServiceDatesList,how='inner',left_on='ID',right_on='ID')

#Rearrange the coloumns in the the order mentioned in the assignment
FullInventory=FullInventory[["ID","Manufacturer Name","Item Type","Price","Service Date","Damaged"]]
#Sort file alphabetically by manufacturer
FullInventory=FullInventory.sort_values('Manufacturer Name')

#Export the Full inventory to a CSV file
FullInventory.to_csv(r'FullInventory.csv',index = False,header=False)

#------Part b(Item Type Inventory)--------

#Obtain items that fall in laptop category
LaptopInventory=FullInventory.loc[FullInventory['Item Type'] == "laptop"]
#Obtain items that fall in phone category
PhoneInventory=FullInventory.loc[FullInventory['Item Type'] == "phone"]
#Obtain items that fall in tower category
TowerInventory=FullInventory.loc[FullInventory['Item Type'] == "tower"]

#Sort items according to their item ID
LaptopInventory=LaptopInventory.sort_values('ID')
PhoneInventory=PhoneInventory.sort_values('ID')
TowerInventory=TowerInventory.sort_values('ID')

LaptopInventory.to_csv(r'LaptopInventory.csv',index=False,header=False)
PhoneInventory.to_csv(r'PhoneInventory.csv',index=False,header=False)
TowerInventory.to_csv(r'TowerInventory.csv',index=False,header=False)



#----------Part c(Past Service Date Inventory)-------------

#Get the today's date
today=datetime.date.today()
today=pd.to_datetime('today')

#Converting the Dataset Service Date column to convert to DateTime to compare with today's date
FullInventory['Service Date']=pd.to_datetime(FullInventory['Service Date'])
#Checking the items that are past the service date on today
PastServiceDateInventory= FullInventory[FullInventory['Service Date']<today]

#Sort the items in the order of service date from oldest to most recent
PastServiceDateInventory=PastServiceDateInventory.sort_values('Service Date')

#Export the data to a PastServiceDateInventory.csv
PastServiceDateInventory.to_csv(r'PastServiceDateInventory.csv ',index=False,header=False)



#----Part d(Damaged Items Inventory)--------

#Check which items are damaged
Damaged=FullInventory.loc[FullInventory['Damaged'] == "damaged"]
#Just to del the damaged columns
del Damaged['Damaged']
#Sorted items in order of most expensive to least expensive
Damaged=Damaged.sort_values('Price',ascending=False)

#Export the Damaged products data to the DamagedInventory.csv
Damaged.to_csv(r'DamagedInventory.csv ',index=False,header=False)



#---------------  Part 2  -------------------------
#-------Interactive Inventory Query ---------------

choice='y'
while(choice!='q'):
    # prompt for user input for the manufacturer
    print('Enter the Manufacturer:')
    manufacturer = input()
    print('Enter the Item Type:')
    item_type = input()
    results=FullInventory.loc[(FullInventory['Manufacturer Name'] == manufacturer) & (FullInventory['Item Type'] == item_type)]
    # Move out items that have passed their service date
    results = results[results['Service Date'] > today]
    # MOve out items that are damaged
    results = results[results['Damaged'] != 'damaged']
    del results['Damaged']
    del results['Service Date']
    if results.empty:
    # If there is no item ony user defined item type show an error message
        print('No such Item in Inventory')
    else:
        # Show the item type which has max price
        print('Your item is:')
        results=results.to_string(index=False)

        print(results)

    #Ask the user if he wants to search again
    print('Do you want to search again (q for quit and y for yes)?')
    choice=input()[0]
    #Check if the user input is valid or not
    while(choice!='q' and choice !='y'):
        print('Invalid Input')
        print('Do you want to search again (q for quit and y for yes)?')
        choice=input()[0]




