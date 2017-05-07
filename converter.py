# ((x - (WIDTH/2))/HEIGHT)*2 = x
# ((z - (HEIGHT/2))/HEIGHT)*2 = z
WIDTH = 484
HEIGHT = 568
x1 = 322 #x kiri atas gedung
x2 = 415 #x kanan atas gedung

z1 = 347 #z atas
z2 = 368 #z bawah

h = 0.01
w1 = ((x1 - (WIDTH/2))/HEIGHT)*2
z1 = ((z1 - (HEIGHT/2))/HEIGHT)*2
w2 = ((x2 - (WIDTH/2))/HEIGHT)*2
z2 = ((z2 - (HEIGHT/2))/HEIGHT)*2
h = -1 + h
print ('[%f, -1, %f],'%(w1,z1))
print ('[%f, -1, %f],'%(w2,z1))

print ('[%f, -1, %f],'%(w2,z2))
print ('[%f, -1, %f],'%(w1,z2))

print ('[%f, %f, %f],'%(w1,h,z1))
print ('[%f, %f, %f],'%(w2,h,z1))
print ('[%f, %f, %f],'%(w2,h,z2))
print ('[%f, %f, %f],'%(w1,h,z2))