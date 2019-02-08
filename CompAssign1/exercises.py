import random
# #exercise 1
# name = input("add your name")
# age = int(input("add your age"))
#
# print("your name is " + name + "and your age is " + str(age))
#

#exercise 2
#
# number = int(input("Pick a number"))
# mod = number % 2
#
# if mod > 0: # even or odd
#     print("Your number is odd")
#
# else:
#     print("Your number is even")
#
# if number % 4 == 0:
#     print("the number is a multiple of 4")
#
# else:
#     print("yor number is not a multiple of 4")


#exercise 3
#
# array = [1,2,3,4,5,6,7,8,9,10]
# secondArray = []
#
# for element in array:
#     if element < 5:
#         secondArray.append(element)
# print(secondArray)



# #exercise 4
# number = int(input("Add a number"))
#
# arrayWithDiv = []
# listRange = list(range(1, number+1))
# print(listRange)
#
# for element in listRange:
#     if number % element == 0:
#         arrayWithDiv.append(element)
#
# print("These are your numbers divisors ")
# print(arrayWithDiv)

# exercise 5
# Merge two list not including duplicates

# a = [1,2,3,4,5,6,55,87]
# b = [1,2,3,4,5,6,7,8,9,10]
# c = []
#
# q = range(1, random.randint(1,50))
# w = range(1, random.randint(1,40))
#
# print(q)
# print(w)
#
# for element in q:
#     for number in w:
#         if element == number:
#             c.append(element)
#
# print(c)

#exercise 6 - check if palindrome
#
# input = input("Chose a string you think is a palindrome ")
# word = str(input)
# rvs = word[::-1]
#
# if rvs == input:
#     print(word + " is a palindrome")

#exercise 7 - return list with even elements in
#
# a = [10, 3, 5, 6, 8, 14]
# c = []
#
# for element in a:
#     if element % 2 == 0:
#         c.append(element)
# print(c)
#
# b = [element for element in a if element % 2 == 0] #smarter way
# print(b)



# rock, paper and scissors

player1 = input("Rock, paper, scissors?")
player2 = input("Rock, paper, scissors?")

# if player1 == player2:
#     print("Even game")
#
# if player1 ==














