def print_list_and_tuple():
    user_input = input()
    
    generated_list = user_input.split(',')
    generated_tuple = tuple(generated_list)
    
    print(generated_list)
    print(generated_tuple)
    
print_list_and_tuple()