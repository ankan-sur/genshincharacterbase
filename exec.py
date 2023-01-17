###########################################################
#  Computer Project #6
#
#  all Functions
#   open func
#   read func
#   criterion func
#   three criteria func
#   sort func
#   display func
#   options func
#
#  main() 
#       open file, looped
#       option prompt, looped
#       option 1
#           region function, prints
#       option 2
#           input checks and runs criterion function
#       option 3
#           input checks for weapon element and rarity
#       option 4
#            closes
###########################################################

import csv
from operator import itemgetter

NAME = 0
ELEMENT = 1
WEAPON = 2
RARITY = 3
REGION = 4

MENU = "\nWelcome to Genshin Impact Character Directory\n\
        Choose one of below options:\n\
        1. Get all available regions\n\
        2. Filter characters by a certain criteria\n\
        3. Filter characters by element, weapon, and rarity\n\
        4. Quit the program\n\
        Enter option: "

INVALID_INPUT = "\nInvalid input"

CRITERIA_INPUT = "\nChoose the following criteria\n\
                 1. Element\n\
                 2. Weapon\n\
                 3. Rarity\n\
                 4. Region\n\
                 Enter criteria number: "

VALUE_INPUT = "\nEnter value: "

ELEMENT_INPUT = "\nEnter element: "
WEAPON_INPUT = "\nEnter weapon: "
RARITY_INPUT = "\nEnter rarity: "

HEADER_FORMAT = "\n{:20s}{:10s}{:10s}{:<10s}{:25s}"
ROW_FORMAT = "{:20s}{:10s}{:10s}{:<10d}{:25s}"

def open_file():
    inp = input("Enter file name: ")
    while True:
        try:
            fp = open(inp,"r")
            return fp
        except:  
            print("\nError opening file. Please try again.")
            inp = input("Enter file name: ")
            continue
            
def read_file(fp):
    master_list = []
    reader = csv.reader(fp)
    next(reader,None) #skipping the headers
    for i in reader: 
        if i[0] == '': #these lines turn empty strings into None values
            name = None
        else:
            name = i[0]
        if i[2] == '':
            element = None
        else:
            element = i[2]
        if i[3] == '':
            weapon = None
        else:
            weapon = i[3]
        if i[1] == '': 
            rarity = None
        else:
            rarity = int(i[1]) #only value that needs to ensure int status
        if i[4] == '':
            region = None
        else:
            region = i[4]
        line_list = [name,element,weapon,rarity,region] #binding all the information 
        line_tup = tuple(line_list)         #into a list and then converting to tuple
        master_list.append(line_tup)
    return master_list

def get_characters_by_criterion (fp, criteria, value):
    returnlist = []
    for i in fp:
        if i[criteria] == None: #since criteria fits index, using the variable instead
            continue            # makes more sense, skips None values 
        list_val = i[criteria]

        if criteria == RARITY: #determining if .lower() is needed or int() is
            value = int(value) 
        else:
            value = value.lower()
            list_val = list_val.lower()

        if list_val == value: 
            returnlist.append(i)
    return returnlist
        
def get_characters_by_criteria(master_list, element, weapon, rarity):

    elemlist = get_characters_by_criterion(master_list, ELEMENT, element) #checks for element in master_list
    weaplist = get_characters_by_criterion(elemlist, WEAPON, weapon) #checks for weapon in element list
    rarelist = get_characters_by_criterion(weaplist, RARITY, rarity) #finally checks rarity in weapon list, therefore shaving the criteria down 
    return rarelist #rarity list only includes things that match with the three parameters
    
def get_region_list  (master_list):
    reg_list = []
    for i in master_list: 
        region = i[4]
        if region == None: #skips empty regions
            continue
        reg_list.append(region)
    reg_list = set(reg_list) #removed duplicates because sets cant have duplicates
    reg_list = list(reg_list)
    reg_list.sort() 
    return reg_list

def sort_characters (list_of_tuples):
    lis = sorted(list_of_tuples, key = itemgetter(0)) #long way to sort by first index
    lis = sorted(lis, key = itemgetter(3), reverse=True) #same method to sort rarity
    return lis
    
def display_characters (list_of_tuples):
    if list_of_tuples == []: #empty list prints error message
        print("\nNothing to print.")
    else:
        print("\n{:20s}{:10s}{:10s}{:<10s}{:25s}".format("Character","Element","Weapon","Rarity","Region")) #format copied from doc
        for i in list_of_tuples:
            name = i[0]
            element = i[1]
            weapon = i[2]
            rarity = i[3]
            if i[4] == None: #this step replaces none with "N/A"
                region = "N/A"
            else:
                region = i[4]
            print("{:20s}{:10s}{:10s}{:<10d}{:25s}".format(name,element,weapon,rarity,region))
        
def get_option():
    inp = int(input(MENU))
    options = [1,2,3,4] #to make sure input is in list
    if inp in options:  
        return inp 
    else:
        print(INVALID_INPUT) 


def main():
    options = [1,2,3,4]
    fp = open_file()
    master = read_file(fp)
    while True: #to keep an input loop for options
        op = get_option() 
        if op == 1:                     #regions
            print("\nRegions:")
            lis = get_region_list(master)
            v = ", ".join(lis)
            print(v)
        elif op == 2:                   #single criteria 
            inp = int(input(CRITERIA_INPUT))
            while True: #keeping a prompt looped
                if inp in options:
                    inp2 = input(VALUE_INPUT)
                    if inp == RARITY:
                        try:
                            inp2 = int(inp2)
                        except: 
                            print(INVALID_INPUT)
                            inp = input(CRITERIA_INPUT)
                    lis = get_characters_by_criterion(master,inp,inp2)
                    lis = sort_characters(lis) 
                    display_characters(lis)
                    break
                else:
                    print(INVALID_INPUT)
                    inp = input(CRITERIA_INPUT)
                    break
        elif op == 3:               #three criterias
            el = input(ELEMENT_INPUT)
            we = input(WEAPON_INPUT)
            ra = input(RARITY_INPUT)
            while not ra.isdigit(): #invalid input case
                print(INVALID_INPUT)
                ra = input(RARITY_INPUT) 
            lis = get_characters_by_criteria(master,el,we,ra)
            lis = sort_characters(lis)
            display_characters(lis)
        elif op == 4:
            break       #exits

# DO NOT CHANGE THESE TWO LINES
#These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.  
if __name__ == "__main__":
    main()
    
