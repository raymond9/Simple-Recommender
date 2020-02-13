#Raymond
#Recommender

 
class Review:
    def __init__(self, title, author, rating):
        self.__title = title
        self.__author = author
        self.__rating = int(rating)

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_rating(self):
        return self.__rating

    def __str__(self):
        return ("Title: " + self.__title + " by " + self.__author +
                ", rating = " + str(self.__rating))

 
# Function Name: main
# Parameters: none
# Return Value: none
# Description: prompts user for a set of choices to add, recommend or print out the best book
def main(): 
    intro()
    choice = "temp"
    lines = open("ratings.txt").readlines()
    dictionary = {} 
    mapping(dictionary, lines) 
    while (choice != "quit"):
        choice = str(input("next task? ")).lower()
        if (choice == "recommend"):
            recommend(dictionary)
        elif (choice == "best"):
            best_book(dictionary)
        elif (choice == "add"):
            add(dictionary)
 
# Function Name: intro
# Parameters: none
# Return Value: none
# Description: prints the header
def intro(): 
    print ("Welcome to Book Recommender. Type the word in the")
    print ("left column to do the action on the right.")
    print ("recommend : recommend books for a particular user")
    print ("best      : the book with the highest rating among all users")
    print ("add       : add a new book")
    print ("quit      : exit the program")
 
# Function Name: mapping
# Parameters: dictionary, lines
# Return Value: none
# Description: reads existing users in ratings.txt and maps them to dictionary
def mapping(dictionary, lines): #maps user to a key and title, author, rating (value)
    for i in range (0, len(lines), 4):
        book = Review(lines[i + 1].strip().lower(), lines[i + 2].strip().lower(), lines[i + 3].strip())
        user = lines[i].strip().lower()
        if (not (user in dictionary)):#if dictionary[user] does not exist create a set with the title
            temp = set()
            temp.add(book)
            dictionary[user] = temp 
        else: 
            dictionary[user].add(book)#if dictionary[user] exists add the book information for that user
 
# Function Name: best_book
# Parameters: dictionary
# Return Value: none
# Description: prints out the best overall book
def best_book(dictionary):
    best_dictionary = {}
    highest = 0
    for item in dictionary:
        for value in dictionary[item]:
            title = (value.get_title())
            rating = (value.get_rating())
            if (not (title in best_dictionary)): #if title is not in the dictionary then create an empty set with a rating 
                temp = set()
                temp.add(rating)
                best_dictionary[title] = temp 
            else:
                best_dictionary[title].add(rating)#if title is in the dictionary then add the rating to the existing set
    for key, sets in best_dictionary.items():#iterates through the items in the set
        total = 0
        for values in sets:
            total += values
        average = total / (len(sets))
        if (average > highest):#cumilitive sum
            best_book = key
            highest = average
    print ("The highest rated book is: " + "\n" + (best_book))
    print ("with an overall score of " + str(highest))
 
# Function Name: add
# Parameters: dictionary
# Return Value: none
# Description: add a user to the dictionary if not mapped already, if user is in the dictionary only add the book info and rating
def add(dictionary):
    new_user = str(input("user? ")).lower().strip()
    new_title = str(input("title? ")).lower().strip()
    new_author = str(input("author? ")).lower().strip()
    new_rating = int(input("rating? "))
    new_info = Review(new_title, new_author, new_rating)
    if (type(new_rating) == int):
        if (not (new_user in dictionary)):#if dictionary[new_user] does not exist create a set using the object
            temp = set()
            temp.add(new_info)
            dictionary[new_user] = temp 
        else: 
            dictionary[new_user].add(new_info)#if dictionary[new_user] exists add the book information for that user
 
# Function Name: recommend
# Parameters: dictionary
# Return Value: none 
# Description: recommends to best book to read based on what the user likes and comparing to other users ratings
def recommend(dictionary):
    recommend_dict = {}
    similar = -1000000000000000
    user = str(input("user? ")).lower().strip()
    if (user in dictionary):
        for value in dictionary[user]: #initialize values for user inputted title and rating
            user_rating = value.get_rating()
            user_title = value.get_title()
            for key in dictionary.keys():
                for value in dictionary[key]:
                    if (key != user):
                        others_title = value.get_title()         
                        others_rating = value.get_rating()
                        if (others_title == user_title):
                            if (not (key in recommend_dict)):
                                recommend_dict[key] = 0
                            recommend_dict[key] += user_rating * others_rating #calculates the recommended rating of the user to other people mapped in dictionary
    if (len(recommend_dict) != 0): #only executes if the inputed user has a read a book that others have
        for key in recommend_dict.items():
            if (key[1] > similar):
                similar = key[1]
                best_user = key[0]
        for value in dictionary[best_user]: #compares the books of the user to the other user and recommends books that user has not read with ratings over 0
            title = value.get_title()
            match = False
            for book in dictionary[user]:
                if (book.get_title() == value.get_title()):
                    match = True
            if (not(match) and value.get_rating() > 0):
                print (value)
main()
