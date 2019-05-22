import numpy as np
import matplotlib.pyplot as plt
y = [9, 10, 9, 11, 10, 11, 10, 12, 12, 11, 13, 12, 13, 13, 14, 13, 14, 14, 15, 14, 15]
z = []
for yi in y:
    if len(z):
        z.append(z[-1]+yi)
    else:
        z.append(yi)
x = [x+1 for x in range(len(y))]
#plt.xlim(1, 21)
plt.plot(x, z)
plt.xlabel('number($x10^7$)')
plt.ylabel('time/s')
plt.show()
z1 = np.polyfit(x, z, 1)
p1 = np.poly1d(z1)
print(p1(1000))
