# ((x - (WIDTH/2))/HEIGHT)*2 = x
# ((z - (HEIGHT/2))/HEIGHT)*2 = z
WIDTH = 484
HEIGHT = 568
x1 = 256 #x kiri atas gedung
z1 = 282 #z atas
x2 = 347 #x kanan atas gedung
z2 = 312 #z bawah
h = 0.08
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