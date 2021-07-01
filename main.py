
#Import Statements===================================================================================================================================================
from bs4 import BeautifulSoup
from numpy.core.fromnumeric import sort
import requests
import csv
from prettytable import PrettyTable
import numpy
import difflib
#====================================================================================================================================================================

#Global Variables
field_list = ["Name","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered","New Recovered","Active Cases","Serious Cases","Total Tests","Population"]

#Updates data within the csv file every time this method is called===================================================================================================    
def on_startup_data_entry():
    url = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(url,"lxml")
    complete_data = []
    world_data = soup.find("tbody").find_all("tr")
    for i in range(8,229):
        data = []
        list_data = world_data[i].find_all("td")
        for i in list_data:
            data.append(i.text)
        complete_data.append(data)
    
    mapped_data = list(map(lambda x: x[1:10] + [x[12]] +[x[14]],complete_data))
  
    
    
    with open("Country_Data.csv","w",newline = "") as csvfile:
        fout = csv.writer(csvfile,delimiter = ",")
        fout.writerow(field_list)
        fout.writerows(mapped_data)
#====================================================================================================================================================================


#Global Statistics Function=========================================================================================================================================
def get_global_stats():
    url = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(url,"lxml")

    global_count = soup.find_all("div",class_ = "maincounter-number")
    
    print("Total No. of Cases in the world:",global_count[0].text.strip())
    print("Total No. of Deaths in the world:",global_count[1].text.strip())
    print("Total No. of Recovered Cases in the world:",global_count[2].text.strip())
#====================================================================================================================================================================


#To print full data table======================================================================================================================================================
def show_complete_data():
    with open("Country_Data.csv","r") as csvfile:
        fin = list(csv.reader(csvfile,delimiter = ","))
        table = PrettyTable(field_names= fin[0])
        table.add_rows(fin[1:])
    print(table)
#====================================================================================================================================================================

#For filtering data==================================================================================================================================================
def sort_data_by_country():
    with open("Country_Data.csv","r") as csvfile:
        fin = list(csv.reader(csvfile,delimiter = ","))
        full_data = fin[1:]
    country = input("Enter the name of the country for which you need data: ")
    print("Getting closest matches in the decreasing order of cases.....")
    closest_list = difflib.get_close_matches(country,get_country_list())
    filtered_country_data = list(filter(lambda x: x[0] in closest_list,full_data ))

    table = PrettyTable(field_names=field_list)
    table.add_rows(filtered_country_data)
    print(table)
#====================================================================================================================================================================
    
#Extra Functions=====================================================================================================================================================
def get_country_list():
    with open("Country_Data.csv","r") as csvfile:
        fin = list(csv.reader(csvfile,delimiter = ","))
        return list(map(lambda x: x[0],fin[1:]))
#====================================================================================================================================================================



#Driver Code=========================================================================================================================================================
if __name__ == "__main__":
    on_startup_data_entry()
    main_Table = PrettyTable(field_names=["Choice","Task"])
    main_Table.add_row([1,"Get data about a particular country"])
    main_Table.add_row([2,"Get data about all the countries"])
    main_Table.add_row([3,"Get global statistics"])
    main_Table.add_row([4,"Exit"])
    while True:
        print(main_Table)
        ch = int(input("Enter Choice: "))
        if ch == 1:
            sort_data_by_country()
        if ch == 2:
            show_complete_data()
        if ch == 3:
            get_global_stats()
        if ch == 4:
            print("Leaving....")
            break
        print("\n"*5)
print("Out of the program. Thank You!!")



    


    




