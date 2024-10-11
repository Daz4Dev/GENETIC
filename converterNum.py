# Description: This program converts a number to required circuit notation.
def conv2seq(num):
     
         # if input number does not have a decimal point, then add it 
    if '.' not in str(num) and 'e' not in str(num):
        num = str(num) + '.0'
        num = float(num)
    
    if(num < 1):
        sign_exponent = 1
        num = '{:.6f}'.format(num)     # override scientific notation
    else:
        sign_exponent = 0
    
    number_string = str(num)

    # Split the string into two parts: the integer part and the decimal part.
    integer_part, decimal_part = number_string.split(".")

    # If the integer part is empty, add a leading zero.
    if not integer_part:
      integer_part = "0"

    # Count the number of digits in the integer part.
    integer_part_length = len(integer_part)

    # If the integer part is longer than one digit, move the decimal point to the
    # right of the first digit.
    if integer_part_length > 1:
      decimal_part = integer_part[1:] + decimal_part
      integer_part = integer_part[0]

    neg_exp = 0
    # if integer part is 0, then change decimal and integer parts till first non-zero digit is integer part
    if integer_part == '0':
        for i in range(len(decimal_part)):
            if decimal_part[i] != '0':
                integer_part = decimal_part[i]
                decimal_part = decimal_part[i+1:]
                neg_exp = i+1
                break


     # make size of decimal part to 6
    if len(decimal_part) > 6:
        decimal_part = decimal_part[:6]
    elif len(decimal_part) < 6:
        decimal_part = decimal_part + '0'*(6-len(decimal_part))

    # Add the exponent to the end of the string.
    if sign_exponent == 0:
        exponent = integer_part_length - 1
    else:
        exponent = neg_exp
    
    scientific_notation_string = integer_part + decimal_part + str(sign_exponent) + str(exponent)

    return scientific_notation_string

# reverse conversion
def seq2conv(num):
    num = str(num)
    integer_part = num[0]
    decimal_part = num[1:7]
    sign_exponent = num[7]
    exponent = int(num[8])
    if sign_exponent != '0':
        exponent = -exponent
    num = integer_part + '.' + decimal_part
    num = float(num) * (10**exponent)
    return num

# x = conv2seq(113.2)
# print(x)
#y = 0.520428
#print(y)
#y_conv = conv2seq(y)
#print(y_conv)   
#z = 1.234234234
#z_c = conv2seq(z)
#print(z_c)