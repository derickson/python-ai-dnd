
def oxfordize(my_list):
    if len(my_list) == 0:
        formatted_str = ""
    elif len(my_list) == 1:
        formatted_str = my_list[0]
    elif len(my_list) == 2:
        formatted_str = " and ".join(my_list)
    else:
        formatted_str = ", ".join(my_list[:-1]) + ", and " + my_list[-1]
    
    return formatted_str
