import CircuitEquivalentEC13 as CE
import numpy as np
from converterNum import conv2seq, seq2conv

R1 = 200
R2 = 200
Rs = 25

R = [R1,   Rs,   0,    0,     R2,    0,     0,     0     ]             
L = [0,    0,    0,    0,     0,     0,     0,     0     ]    
C = [0,    0,    0,    0,     0,     0,     0,     0     ]      
W = [0,    0,    0,    0,     0,     0,     0,     0     ]      
Y = [0,    0,    0,    0,     0,     0,     0,     0     ]    
n = [0,    0,    0,    0,     0,     0,     0,     0     ]    
                                                              
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

#f = CE.dec_step(1e-2, 1e5, 72)
f = 10
res = CE.gen_freq_response(E, f)

print(res)