from ast import literal_eval as make_tuple

class petaITB(object):
	vertices = ""
	
	'''
	with open("res/bangunan.txt") as f:
		z1 = 0
		z2 = 10
		lines = f.readlines()
		vertex = []

		for i in lines:
			line = i.split('|')
			for j in line:
				if (j.find('*') == -1):
					point = j.split(',')
					vertex.append(make_tuple('(%s,%s,%s), ' % (point[0], z1, point[1])))
			for j in line:
				if (j.find('*') == -1):
					point = j.split(',')
					vertex.append('(%s,%s,%s), ' % (point[0], z2, point[1]))
		
		vertex = "".join(vertex)	
		vertex = vertex[:-2]
		vertices = '(%s)' % (vertex)
		'''
		
	with open("res/bangunan.txt") as f:
		z1 = 0
		z2 = 10
		lines = f.readlines()
		vertices = []
		vertice = []
		
		#counter = 0
		for i in lines:
			line = i.split('|')
			for j in line:
				if (j.find('*') == -1):
					point = j.split(',')
					vertices.append(make_tuple('(%s,%s,%s)' % (point[0], z1, point[1])))
			for j in line:
				if (j.find('*') == -1):
					point = j.split(',')
					vertices.append(make_tuple('(%s,%s,%s)' % (point[0], z2, point[1])))
					
			vertice.append(tuple(vertices))
		
			del vertices[:]
			#counter = counter + 1

	print(vertice)

def main():
	peta = petaITB()
