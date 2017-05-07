# ((x - (WIDTH/2))/HEIGHT)*2 = x
# ((z - (HEIGHT/2))/HEIGHT)*2 = z
WIDTH = 484
HEIGHT = 568

x_real = [87, 135, 135, 87] 
z_real = [288, 288, 306, 306]

h = 0.05

x = [float(x - (WIDTH / 2)) / HEIGHT * 2 for x in x_real]
z = [float(z - (WIDTH / 2)) / HEIGHT * 2 for z in z_real]

h = -1 + h
for i in range(len(x)):
	print ('[%f, -1, %f],'%(x[i],z[i]))

for i in range(len(x)):
	print ('[%f, %f, %f],'%(x[i],h,z[i]))

