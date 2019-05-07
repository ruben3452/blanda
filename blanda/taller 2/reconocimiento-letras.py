#Ruben Dario Acuña Ocampo 
# A - E - I - O - U 
''' A - E - I - O - U '''
import numpy as np
import neurolab as nl
                                                                         
target =  [[0,0,1,0,0,
            0,1,0,1,0,
            1,0,0,0,1,
            1,1,1,1,1,
            1,0,0,0,1],
          [ 1,1,1,1,1,
            1,0,0,0,0,
            1,1,1,1,1,
            1,0,0,0,0,
            1,1,1,1,1],
          [ 1,1,1,1,1,
            0,0,1,0,0,
            0,0,1,0,0,
            0,0,1,0,0,
            1,1,1,1,1],
          [ 1,1,1,1,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,1,1,1,1],
           [1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,1,0,1,1,
            0,1,1,1,0]]

chars = ['A', 'E', 'I', 'O','U']
target = np.asfarray(target)
target[target == 0] = -1

net = nl.net.newhop(target)

output = net.sim(target)
print("Test on train samples:")
for i in range(len(target)):
    print(chars[i], (output[i] == target[i]).all())

print("\nTest on defaced A:")
test =np.asfarray([0,0,1,0,0,
                   0,1,0,1,0,
                   0,1,1,1,0,
                   0,1,0,1,0,
                   0,1,0,1,0])
test[test==0] = -1
out = net.sim([test])
print ((out[0] == target[0]).all(), 'Sim. steps',len(net.layers[0].outs))