# ((x - (WIDTH/2))/HEIGHT)*2 = x
# ((z - (HEIGHT/2))/HEIGHT)*2 = z

import sys
WIDTH = 484
HEIGHT = 568

x_real = [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])] 
z_real = [float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8])]

h = float(sys.argv[9])

x = [float(x - (WIDTH / 2)) / HEIGHT * 2 for x in x_real]
z = [float(z - (HEIGHT / 2)) / HEIGHT * 2 for z in z_real]

h = -1 + h
for i in range(len(x)):
	print ('[%f, -1, %f],'%(x[i],z[i]))

for i in range(len(x)):
	print ('[%f, %f, %f],'%(x[i],h,z[i]))

