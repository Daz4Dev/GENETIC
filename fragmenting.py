
def len_complex(vector):
    """
    Calculate the number of complex numbers in a vector, which can be either a single complex number
    or a list of complex numbers.

    Args:
    vector (complex or list of complex): The vector represented as either a single complex number
        or a list of complex numbers.

    Returns:
    int: The number of complex numbers in the vector.
    """
    if isinstance(vector, complex):
        return 1
    elif isinstance(vector, list):
        return len(vector)
    else:
        raise TypeError("Input must be either a complex number or a list of complex numbers.")



'''
This function iterates through each element of Z and F simultaneously. 
It appends elements from Z to a current sublist until it encounters a 1 in F or reaches the end of the lists. 
At that point, it appends the current sublist to the result list and starts a new sublist. Finally, it returns the resulting list of lists.
'''


def split_vector(Z, F):
    result = []
    current_sublist = []
    
    for i in range(len(Z)):
        current_sublist.append(Z[i])
        
        if F[i] == 1 or i == len(Z) - 1:
            result.append(current_sublist)
            current_sublist = []
    
    return result

'''
In this code, process_entry function takes an entry vector and checks its length. 
If the length is 1, it returns the entry as it is. Otherwise, it sums up all the elements and returns a single-value vector. 
The process_vector_of_vectors function iterates over the input vector and applies process_entry function to each entry, building the resulting vector.
'''

# def process_entry(entry):
#     if len_complex(entry) == 1:
#         return entry[0]
#     else:
#         return [sum(entry)]

def process_entry(entry):
    if isinstance(entry, (int, float, complex)):
        return entry
    elif isinstance(entry, list):
        if len(entry) == 1:
            return entry[0]
        else:
            return sum(process_entry(item) for item in entry)
    elif isinstance(entry, complex):
        return entry.real + entry.imag
    else:
        print(type(entry))
        raise ValueError("Unsupported data type in entry")
        

def process_vector_of_vectors(input_vector):
    result = []
    for entry in input_vector:
        result.append(process_entry(entry))
    return result

'''
In this implementation, the flatten_vector function iterates over each item in the input vector. 
If an item is a list, it recursively calls itself to flatten the nested structure. 
Otherwise, it appends the item to the result. Finally, it returns the flattened result.
'''
def flatten_vector(input_vector):
    result = []
    for item in input_vector:
        if isinstance(item, list):
            result.extend(flatten_vector(item))
        else:
            result.append(item)
    return result

'''
This code defines a function calculate_new_vector that takes two input vectors top and bottom. 
It iterates over their elements simultaneously, calculates the new value using the provided formula, and appends it to the new vector. 
Finally, it returns the new vector.
'''
def calculate_eq_vector(top, bottom):
    new_vector = []
    for i in range(len(top)):
        ai = top[i]
        bi = bottom[i]
        new_element = 1 / (1 / ai + 1 / bi)
        new_vector.append(new_element)
    return new_vector

