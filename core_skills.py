import random
rand_list = random.choices(range(1,21),k=10)

list_comprehension_below_10 = [num for num in rand_list if num<10]

list_comprehension_below_10 = list(filter(lambda x:x<10,rand_list))