# ((x - (WIDTH/2))/HEIGHT)*2 = x
# ((z - (HEIGHT/2))/HEIGHT)*2 = z

import sys
WIDTH = 484
HEIGHT = 568


# x_real = [369, 407, 408, 372] 
# z_real = [61, 64, 18, 16]


# x_real = [173, 207, 207, 173] 
# z_real = [501, 501, 484, 484]

# x_real = [191, 228, 225, 187] 
# z_real = [374, 374, 354, 356]

# x_real = [40, 79, 79, 40] 
# z_real = [430, 430, 405, 405]

# x_real = [210, 230, 230, 210] 
# z_real = [524, 524, 510, 510]

# x_real = [88, 173, 173, 88] 
# z_real = [440, 440, 415, 415]

# x_real = [44, 73, 73, 44] 
# z_real = [400, 400, 390, 390]

# x_real = [93, 165, 165, 93] 
# z_real = [410, 410, 368, 368]

# x_real = [47, 78, 78, 47] 
# z_real = [385, 385, 355, 355]


# h = 0.01

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

