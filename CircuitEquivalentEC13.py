from converterNum import conv2seq, seq2conv
import numpy as np
import fragmenting as frag


R1 = 500                                                       
Rs = 20                                                       
R2 = 1000                                                      
Y1 = 0.00001                                                   
n1 = 0.9                                                      
A1 = 250                                                      
                                                              
R = [R1,   Rs,   0,    0,     R2,    0,     0,     0     ]             
L = [0,    0,    0,    0,     0,     0,     0,     0     ]    
C = [0,    0,    0,    0,     0,     0,     0,     0     ]      
W = [A1,   0 ,   0,    0,     0,     0,     0,     0     ]      
Y = [Y1,   0,    0,    0,     0,     0,     0,     0     ]    
n = [n1,   0,    0,    0,     0,     0,     0,     0     ]    
                                                              
Connects = [1,1,0,0,0]                                        

# convert all values in vector R into the forms produced by conv2seq
R_seq = [conv2seq(r) for r in R]
L_seq = [conv2seq(l) for l in L]
C_seq = [conv2seq(c) for c in C]
W_seq = [conv2seq(w) for w in W]
Y_seq = [conv2seq(y) for y in Y]
n_seq = [conv2seq(n) for n in n]



# concatenate respective indices of R_seq,L_seq,C_seq
E = [R_seq[i] + L_seq[i] + C_seq[i] + W_seq[i] + Y_seq[i] + n_seq[i] for i in range(len(R_seq))]
# concatenate all entries of E into a single string
E = ''.join(E)
# concatenate E with connects
E = E + ''.join([str(c) for c in Connects])


# get R,L,C,W,Y,n,connects from E
# get locations, from it get values of components in the string


def get_component_values(E):
    R_index_values = []
    start_index = 0
    while start_index <= 423:
        R_index_values.append(start_index)
        R_index_values.append(start_index+9)
        start_index += 54

    R_rev_std = [E[R_index_values[i]:R_index_values[i+1]] for i in range(0,len(R_index_values),2)]
    R_rev = [seq2conv(r) for r in R_rev_std]
    L_rev_std = [E[R_index_values[i]+9:R_index_values[i+1]+9] for i in range(0,len(R_index_values),2)]
    L_rev = [seq2conv(l) for l in L_rev_std]
    C_rev_std = [E[R_index_values[i]+18:R_index_values[i+1]+18] for i in range(0,len(R_index_values),2)]
    C_rev = [seq2conv(c) for c in C_rev_std]
    W_rev_std = [E[R_index_values[i]+27:R_index_values[i+1]+27] for i in range(0,len(R_index_values),2)]
    W_rev = [seq2conv(w) for w in W_rev_std]
    Y_rev_std = [E[R_index_values[i]+36:R_index_values[i+1]+36] for i in range(0,len(R_index_values),2)]
    Y_rev = [seq2conv(y) for y in Y_rev_std]
    n_rev_std = [E[R_index_values[i]+45:R_index_values[i+1]+45] for i in range(0,len(R_index_values),2)]
    n_rev = [seq2conv(n) for n in n_rev_std]

    Connects_rev = [int(c) for c in E[432:]]

    return R_rev, L_rev, C_rev, W_rev, Y_rev, n_rev, Connects_rev

R_rev, L_rev, C_rev, W_rev, Y_rev, n_rev, Connects_rev = get_component_values(E)

# print("----R_rev:----")
# print(R_rev)
# print("----L_rev:----")
# print(L_rev)
# print("----C_rev:----")
# print(C_rev)
# print("----W_rev:----")
# print(W_rev)
# print("----Y_rev:----")
# print(Y_rev)
# print("----n_rev:----")
# print(n_rev)
# print("----Connects_rev:----")
# print(Connects_rev)


# print("----Connects_rev:----")
# print(Connects_rev)


# Rares = [E[R_index_values[i]:R_index_values[i+1]] for i in range(0,len(R_index_values),2)]
# print("----R_ares:----")
# print(Rares)
# print("----R_seq:----")
# print(R_seq)




# generating frequency response
def gen_freq_response(E,f):
    w = 2*np.pi*f
    Z_block = [0+0j]*8
    R_rev, L_rev, C_rev, W_rev, Y_rev, n_rev, Connects_rev = get_component_values(E)

    
    Z_CPE = [0+0j]*8
    Z_C = [0+0j]*8

    # invisible link
    # Connects_rev.append(0)

    for i in range(8):
        
        # checking for Y
        if Y_rev[i] < 1e-6:
            Z_CPE[i] = 1e12
        else:
            Z_CPE[i] = 1/Y_rev[i]*((1j*w)**n_rev[i])

        # checking for R
        if R_rev[i] < 1e-6:     # was 0 here in rhs
            R_rev[i] = 1e-12
        
        # checking for W    
        if W_rev[i] < 1e-6:
            W_rev[i] = 1e-12

        #LATEST ADDITIONS : 136 to 149 ; eqn modified 152
            # Capacitor edge case
        if C_rev[i] < 1e-6:
            Z_C[i] = 1e12
        else:
            Z_C[i] = 1/(w*C_rev[i])

            # complex n
        if n_rev[i] != abs(n_rev[i]):
            n_rev[i] = abs(n_rev[i])

            # Inductor edge case
        if L_rev[i] < 1e-6:
            L_rev[i] = 1e-12

        # generic formula for Z_block
        Z_block[i] = 1/(  1/(  R_rev[i] + (W_rev[i]*(1-1j)/(w**0.5)) + 1j*w*L_rev[i]  )  +  1/(  (Z_CPE[i]) + (Z_C[i])  )  )
        #                 ---------------------------1/Zt------------------------------     ---------------1/Zb-------------

        # only bottom row is present in block
        if R_rev[i] == 1e-12 and W_rev[i] == 1e-12 and L_rev[i] == 1e-12:
            Z_block[i] = Z_CPE[i] + Z_C[i]

        # only top row is present in block : no effect as values adjusted previously
        # T are 155 to 160 redundant?
        
        
        # Empty block
        
        Empty = ((R_rev[i] == 1e-12) and (W_rev[i] == 1e-12) and (L_rev[i] == 1e-12) and (Y_rev[i] <1e-6) and (C_rev[i] < 1e-6)) 
      
        if Empty:
            Z_block[i] = 1e-12 + 0j
         

    Z_top = Z_block[:4]
    Z_bottom = Z_block[4:]

        
    Connects_top = Connects_rev[1:]
    Connects_bottom = Connects_rev[1:]

    Z_top = frag.split_vector(Z_top, Connects_top)
    Z_bottom = frag.split_vector(Z_bottom, Connects_bottom)

    # debugging
    print("----Z_top:----")
    print(Z_top)
    print("----Z_bottom:----")
    print(Z_bottom)

    Z_top_processed = [frag.process_entry(entry) for entry in Z_top]
    Z_bottom_processed = [frag.process_entry(entry) for entry in Z_bottom]


    Z_top_flattened = frag.process_vector_of_vectors(Z_top_processed)
    Z_bottom_flattened = frag.process_vector_of_vectors(Z_bottom_processed)


    Z_eq = frag.calculate_eq_vector(Z_top_flattened, Z_bottom_flattened)

    Z_total = sum(Z_eq)

    
    Z_total_real = np.real(Z_total)
    Z_total_imag = np.imag(Z_total)

    Z_total = np.column_stack((Z_total_real, Z_total_imag))

    nested_vector = Z_total

    Z_total = [element for sublist in nested_vector for element in sublist]

    # if f == 1e-2:
    #     print("----Z_total:----")
    # print(Z_total)

    return Z_total
    
    '''
    Z_parallel is a list. The list comprehension [1/(1/Z_block[i] + 1/Z_block[i+4]) if Connects_rev[i] == 1 and Connects_rev[i+1] == 1 else Z_block[i] for i in range(4)] is used to generate the elements of the Z_parallel list.

    The list comprehension iterates over the range(4) object, which represents a sequence of integers from 0 to 3. 
    For each iteration, it checks the conditions Connects_rev[i] == 1 and Connects_rev[i+1] == 1. 
    If both conditions are true, it calculates the value 1/(1/Z_block[i] + 1/Z_block[i+4]) and adds it to the Z_parallel list. 
    Otherwise, it adds the value Z_block[i] to the list.
    
    '''

def dec_step(start, end, steps, roundTo=2):
    log_list = np.logspace(np.log10(start), np.log10(end), num=steps)
    return np.array([round(i, roundTo) for i in log_list])

E1 = E

f = dec_step(1e-2, 1e5, 72)
Z_total = np.array([gen_freq_response(E1,freq) for freq in f])
#Z_total = [gen_freq_response(E1,1e5)]
# print("----Z_total:----")
# print(Z_total)

# split Z_total into real and imaginary parts



# add the real and imaginary parts to get single matrix with two columns, one for real, other for imaginary


# print("----Z_total:----")
# print(Z_total)

# Z1 = [674.45510657-138.22977605j ,674.45510657-138.22977605j,
#       608.29169157-132.02832098j ,608.29169157-132.02832098j,
#       608.29169157-132.02832098j ,572.28035389-124.67298268j,
#       548.51543996-118.21959203j ,531.24342965-112.70414588j,
#       517.92616858-107.96479661j ,498.40223018-100.23231038j,
#       484.51471306 -94.15430414j ,473.96831811 -89.21487053j,
#       462.01036159 -83.27861247j ,450.43374579 -77.20189662j,
#       440.03215801 -71.48535824j ,430.99568012 -66.35056502j,
#       422.3065462  -61.30812812j ,415.20466418 -57.15850818j,
#       407.798608   -52.87772601j ,401.66319212 -49.45166493j,
#       395.99876727 -46.48696965j ,390.77868886 -44.0440276j,
#       385.9918342  -42.18832833j ,381.61077908 -40.96681371j,
#       377.43151511 -40.39490766j ,373.37560779 -40.56840996j,
#       369.48635334 -41.55787328j ,365.57143694 -43.45753206j,
#       361.49418626 -46.38336876j ,357.08968051 -50.45661945j,
#       352.15468645 -55.78476152j ,346.36644304 -62.52418974j,
#       339.40865204 -70.69546792j ,330.79923398 -80.32707455j,
#       319.9899637  -91.28230346j ,306.40066446-103.1888049j,
#       289.46736761-115.40183674j ,268.81415144-126.93933948j,
#       244.50867373-136.51703885j ,217.19092596-142.79553168j,
#       188.17235554-144.70539638j ,159.13317891-141.80573427j,
#       131.85742959-134.44152431j ,107.70542446-123.62653122j,
#       87.39136522-110.69243448j  ,71.03604314 -96.95424595j,
#       58.2955058  -83.44497376j  ,48.60546445 -70.84937468j,
#       41.35464335 -59.54138211j  ,35.97991308 -49.65632822j,
#       32.01265756 -41.17802702j  ,29.08471856 -34.00426949j,
#       26.91759103 -27.99311297j  ,25.30550307 -22.99151128j,
#       24.09847923 -18.8511548j   ,23.18796409 -15.43628665j,
#       22.49576264 -12.62768351j  ,21.96534827 -10.32234091j,
#       21.55579735  -8.4330145j   ,21.23728489  -6.88642638j,
#       20.98792769  -5.62151872j  ,20.79154162  -4.58769585j,
#       20.63605264  -3.74318983j  ,20.51237231  -3.05361873j,
#       20.4135987   -2.49074174j  ,20.33444498  -2.03139853j,
#       20.27082932  -1.65662317j  ,20.21957585  -1.35089511j,
#       20.17819745  -1.10152651j  ,20.14473416  -0.89814898j,
#       20.1176334   -0.7322943j   ,20.09565958  -0.59704893j]
    
# print("----Zdiff:----")
# print(Z_total-Z1)

