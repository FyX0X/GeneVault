def geometrical_average(l):
    """
    Calculate the geometrical average of a list of numbers.
    
    :param l: List of numbers
    :return: Geometrical average
    """
    product = 1
    n = len(l)
    
    for num in l:
        product *= num
    
    return product ** (1/n)