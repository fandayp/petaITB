#!/usr/bin/env python

import sys,pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from pygame.constants import *

from OpenGL.arrays import vbo
from OpenGL.GL.shaders import compileProgram, compileShader
from ast import literal_eval as make_tuple

# import from other files in project
import ctypes

from texture import Texture
from display import Display
from shaders.vertexShader import *
from shaders.fragmentShader import *

WIDTH = 800
HEIGHT = 600
rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5

class petaITB(object):
    distance = 0
    #rotation
    x_axis = 0.0
    y_axis = 0.0
    z_axis = 0.0
    vertices = []
    vertice = []

    with open("res/bangunan.txt") as f:
        z1 = 0
        z2 = 10
        lines = f.readlines()

        for i in lines:
            line = i.split('|')
            for j in line:
                if (j.find('*') == -1):
                    point = j.split(',')
                    vertices.append(make_tuple('(%d,%s,%s)' % (int(point[0])-270, z1, point[1])))
            for j in line:
                if (j.find('*') == -1):
                    point = j.split(',')
                    vertices.append(make_tuple('(%d,%s,%s)' % (int(point[0])-270, z2, point[1])))

            vertice.append(tuple(vertices))

            del vertices[:]

    vertOnly = [
        [-0.85, -1, 1],
        [ 0.85, -1, 1],
        [ 0.85, -1, -1],
        [-0.85, -1, -1],

        # Bangunan Labtek VII
        [ 0.062, -1, -0.1514084],#
        [ 0.390, -1, -0.1514084],#
        [ 0.390, -1, -0.08098],
        [ 0.062, -1, -0.08098],
        [ 0.062, -0.95, -0.1514084],#
        [ 0.390, -0.95, -0.1514084],#
        [ 0.390, -0.95, -0.08098],
        [ 0.062, -0.95, -0.08098],

        # Bangunan Labtek VI
        [-0.380282, -1, -0.147887],
        [-0.052817, -1, -0.147887],
        [-0.052817, -1, -0.073944],
        [-0.380282, -1, -0.073944],
        [-0.380282, -0.950000, -0.147887],
        [-0.052817, -0.950000, -0.147887],
        [-0.052817, -0.950000, -0.073944],
        [-0.380282, -0.950000, -0.073944],

        # Bangunan Labtek V
        [-0.345070, -1, 0.014085],
        [-0.042254, -1, 0.014085],
        [-0.042254, -1, 0.098592],
        [-0.345070, -1, 0.098592],
        [-0.345070, -0.950000, 0.014085],
        [-0.042254, -0.950000, 0.014085],
        [-0.042254, -0.950000, 0.098592],
        [-0.345070, -0.950000, 0.098592],

        #Bangungan Labtek VIII
        [0.049296, -1, -0.007042],
        [0.369718, -1, -0.007042],
        [0.369718, -1, 0.098592],
        [0.049296, -1, 0.098592],
        [0.049296, -0.950000, -0.007042],
        [0.369718, -0.950000, -0.007042],
        [0.369718, -0.950000, 0.098592],
        [0.049296, -0.950000, 0.098592],

        #Bangungan Lab UMH
        [0.454225, -1, -0.172535],
        [0.658451, -1, -0.172535],
        [0.658451, -1, -0.102113],
        [0.454225, -1, -0.102113],
        [0.454225, -0.980000, -0.172535],
        [0.658451, -0.980000, -0.172535],
        [0.658451, -0.980000, -0.102113],
        [0.454225, -0.980000, -0.102113],

        #Bangungan GKU Timur
        [0.531690, -1, -0.095070],
        [0.721831, -1, -0.095070],
        [0.721831, -1, 0.000000],
        [0.531690, -1, 0.000000],
        [0.531690, -0.950000, -0.095070],
        [0.721831, -0.950000, -0.095070],
        [0.721831, -0.950000, 0.000000],
        [0.531690, -0.950000, 0.000000],

        #Bangungan Doping
        [0.464789, -1, 0.066901],
        [0.577465, -1, 0.066901],
        [0.577465, -1, 0.133803],
        [0.464789, -1, 0.133803],
        [0.464789, -0.950000, 0.066901],
        [0.577465, -0.950000, 0.066901],
        [0.577465, -0.950000, 0.133803],
        [0.464789, -0.950000, 0.133803],

        #M Tek Geodesi
        [0.644366, -1, 0.010563],
        [0.711268, -1, 0.010563],
        [0.711268, -1, 0.088028],
        [0.644366, -1, 0.088028],
        [0.644366, -0.990000, 0.010563],
        [0.711268, -0.990000, 0.010563],
        [0.711268, -0.990000, 0.088028],
        [0.644366, -0.990000, 0.088028],

        #M.S & T Jil Raya (?)
        [0.654930, -1, 0.098592],
        [0.707746, -1, 0.098592],
        [0.707746, -1, 0.169014],
        [0.654930, -1, 0.169014],
        [0.654930, -0.990000, 0.098592],
        [0.707746, -0.990000, 0.098592],
        [0.707746, -0.990000, 0.169014],
        [0.654930, -0.990000, 0.169014],

        #CC Timur
        [0.091549, -1, 0.242958],
        [0.228873, -1, 0.242958],
        [0.228873, -1, 0.302817],
        [0.091549, -1, 0.302817],
        [0.091549, -0.990000, 0.242958],
        [0.228873, -0.990000, 0.242958],
        [0.228873, -0.990000, 0.302817],
        [0.091549, -0.990000, 0.302817],

        #Altim
        [0.183099, -1, 0.651408],
        [0.274648, -1, 0.651408],
        [0.274648, -1, 0.711268],
        [0.183099, -1, 0.711268],
        [0.183099, -0.990000, 0.651408],
        [0.274648, -0.990000, 0.651408],
        [0.274648, -0.990000, 0.711268],
        [0.183099, -0.990000, 0.711268],

        #LFM
        [0.186620, -1, 0.524648],
        [0.260563, -1, 0.524648],
        [0.260563, -1, 0.595070],
        [0.186620, -1, 0.595070],
        [0.186620, -0.990000, 0.524648],
        [0.260563, -0.990000, 0.524648],
        [0.260563, -0.990000, 0.595070],
        [0.186620, -0.990000, 0.595070],

        #Tekling, HMTL
        [0.281690, -1, 0.221831],
        [0.609155, -1, 0.221831],
        [0.609155, -1, 0.295775],
        [0.281690, -1, 0.295775],
        [0.281690, -0.990000, 0.221831],
        [0.609155, -0.990000, 0.221831],
        [0.609155, -0.990000, 0.295775],
        [0.281690, -0.990000, 0.295775],

        #Labtek IX A
        [0.271127, -1, 0.338028],
        [0.450704, -1, 0.338028],
        [0.450704, -1, 0.415493],
        [0.271127, -1, 0.415493],
        [0.271127, -0.990000, 0.338028],
        [0.450704, -0.990000, 0.338028],
        [0.450704, -0.990000, 0.415493],
        [0.271127, -0.990000, 0.415493],

        #Labtek IX C
        [0.468310, -1, 0.327465],
        [0.637324, -1, 0.327465],
        [0.637324, -1, 0.408451],
        [0.468310, -1, 0.408451],
        [0.468310, -0.990000, 0.327465],
        [0.637324, -0.990000, 0.327465],
        [0.637324, -0.990000, 0.408451],
        [0.468310, -0.990000, 0.408451],

        #Labtek IX B
        [0.471831, -1, 0.450704],
        [0.633803, -1, 0.450704],
        [0.633803, -1, 0.528169],
        [0.471831, -1, 0.528169],
        [0.471831, -0.990000, 0.450704],
        [0.633803, -0.990000, 0.450704],
        [0.633803, -0.990000, 0.528169],
        [0.471831, -0.990000, 0.528169],

        #FSRD
        [0.313380, -1, 0.468310],
        [0.461268, -1, 0.468310],
        [0.461268, -1, 0.528169],
        [0.313380, -1, 0.528169],
        [0.313380, -0.990000, 0.468310],
        [0.461268, -0.990000, 0.468310],
        [0.461268, -0.990000, 0.528169],
        [0.313380, -0.990000, 0.528169],

        #Gedung random pojok kanan bawah
        [0.471831, -1, 0.566901],
        [0.545775, -1, 0.566901],
        [0.545775, -1, 0.707746],
        [0.471831, -1, 0.707746],
        [0.471831, -0.990000, 0.566901],
        [0.545775, -0.990000, 0.566901],
        [0.545775, -0.990000, 0.707746],
        [0.471831, -0.990000, 0.707746],

        #Gedung random pojok kanan bawah 2
        [0.362676, -1, 0.559859],
        [0.454225, -1, 0.559859],
        [0.454225, -1, 0.683099],
        [0.362676, -1, 0.683099],
        [0.362676, -0.990000, 0.559859],
        [0.454225, -0.990000, 0.559859],
        [0.454225, -0.990000, 0.683099],
        [0.362676, -0.990000, 0.683099],
        
        # Bangunan Lab Mesin Metalurgi
		[-0.714789, -1, -0.338028],
		[-0.478873, -1, -0.338028],
		[-0.478873, -1, -0.461268],
		[-0.714789, -1, -0.461268],
		[-0.714789, -0.950000, -0.338028],
		[-0.478873, -0.950000, -0.338028],
		[-0.478873, -0.950000, -0.461268],
		[-0.714789, -0.950000, -0.461268],

        # Bangunan Labtek II
		[-0.707746, -1, -0.137324],
		[-0.577465, -1, -0.137324],
		[-0.577465, -1, -0.211268],
		[-0.707746, -1, -0.211268],
		[-0.707746, -0.950000, -0.137324],
		[-0.577465, -0.950000, -0.137324],
		[-0.577465, -0.950000, -0.211268],
		[-0.707746, -0.950000, -0.211268],

        # Bangunan Labtek XI
		[-0.404930, -1, -0.299296],
		[-0.228873, -1, -0.299296],
		[-0.228873, -1, -0.397887],
		[-0.404930, -1, -0.397887],
		[-0.404930, -0.950000, -0.299296],
		[-0.228873, -0.950000, -0.299296],
		[-0.228873, -0.950000, -0.397887],
		[-0.404930, -0.950000, -0.397887],

        #Bangungan Lab TR_GM
		[-0.718310, -1, 0.088028],
		[-0.605634, -1, 0.088028],
		[-0.605634, -1, 0.038732],
		[-0.718310, -1, 0.038732],
		[-0.718310, -0.950000, 0.088028],
		[-0.605634, -0.950000, 0.088028],
		[-0.605634, -0.950000, 0.038732],
		[-0.718310, -0.950000, 0.038732],

        #Bangungan Lab KEE
		[-0.496479, -1, 0.161972],
		[-0.362676, -1, 0.161972],
		[-0.362676, -1, 0.098592],
		[-0.496479, -1, 0.098592],
		[-0.496479, -0.950000, 0.161972],
		[-0.362676, -0.950000, 0.161972],
		[-0.362676, -0.950000, 0.098592],
		[-0.496479, -0.950000, 0.098592],

		# CRCS
		[0.447183, -1, -0.820423],
		[0.580986, -1, -0.809859],
		[0.584507, -1, -0.971831],
		[0.457746, -1, -0.978873],
		[0.447183, -0.930000, -0.820423],
		[0.580986, -0.930000, -0.809859],
		[0.584507, -0.930000, -0.971831],
		[0.457746, -0.930000, -0.978873],
		
		# Labtek IV
		[0.447183, -1, -0.721831],
		[0.792254, -1, -0.690141],
		[0.795775, -1, -0.739437],
		[0.450704, -1, -0.767606],
		[0.447183, -0.945000, -0.721831],
		[0.792254, -0.945000, -0.690141],
		[0.795775, -0.945000, -0.739437],
		[0.450704, -0.945000, -0.767606],

		# BSC-B
		[0.468310, -1, -0.471831],
		[0.725352, -1, -0.454225],
		[0.728873, -1, -0.489437],
		[0.471831, -1, -0.510563],
		[0.468310, -0.960000, -0.471831],
		[0.725352, -0.960000, -0.454225],
		[0.728873, -0.960000, -0.489437],
		[0.471831, -0.960000, -0.510563],

		# Kimia Atas
		[0.464789, -1, -0.376761],
		[0.693662, -1, -0.352113],
		[0.697183, -1, -0.429577],
		[0.471831, -1, -0.450704],
		[0.464789, -0.980000, -0.376761],
		[0.693662, -0.980000, -0.352113],
		[0.697183, -0.980000, -0.429577],
		[0.471831, -0.980000, -0.450704],
		
		# Kimia Bawah
		[0.457746, -1, -0.281690],
		[0.714789, -1, -0.257042],
		[0.721831, -1, -0.320423],
		[0.464789, -1, -0.345070],
		[0.457746, -0.980000, -0.281690],
		[0.714789, -0.980000, -0.257042],
		[0.721831, -0.980000, -0.320423],
		[0.464789, -0.980000, -0.345070],
		
		#tvst
		[-0.098592, -1, -0.394366],
		[-0.024648, -1, -0.323944],
		[-0.088028, -1, -0.253521],
		[-0.169014, -1, -0.323944],
		[-0.098592, -0.930000, -0.394366],
		[-0.024648, -0.930000, -0.323944],
		[-0.088028, -0.930000, -0.253521],
		[-0.169014, -0.930000, -0.323944],
		
		#oktagon
		[-0.084507, -1, -0.559859],
		[-0.021127, -1, -0.496479],
		[-0.088028, -1, -0.422535],
		[-0.161972, -1, -0.489437],
		[-0.084507, -0.930000, -0.559859],
		[-0.021127, -0.930000, -0.496479],
		[-0.088028, -0.930000, -0.422535],
		[-0.161972, -0.930000, -0.489437],

		#fidas
		[0.088028, -1, -0.454225],
		[0.214789, -1, -0.454225],
		[0.207746, -1, -0.524648],
		[0.045775, -1, -0.528169],
		[0.088028, -0.930000, -0.454225],
		[0.214789, -0.930000, -0.454225],
		[0.207746, -0.930000, -0.524648],
		[0.045775, -0.930000, -0.528169],
		
		#power
		[0.056338, -1, -0.313380],
		[0.225352, -1, -0.316901],
		[0.214789, -1, -0.397887],
		[0.080986, -1, -0.390845],
		[0.056338, -0.930000, -0.313380],
		[0.225352, -0.930000, -0.316901],
		[0.214789, -0.930000, -0.397887],
		[0.080986, -0.930000, -0.390845],
		
		#labtek 1
		[0.271127, -1, -0.570423],
		[0.348592, -1, -0.573944],
		[0.341549, -1, -0.334507],
		[0.260563, -1, -0.327465],
		[0.271127, -0.930000, -0.570423],
		[0.348592, -0.930000, -0.573944],
		[0.341549, -0.930000, -0.334507],
		[0.260563, -0.930000, -0.327465],
		
		#lab bahan	
		[0.271127, -1, -0.316901],
		[0.362676, -1, -0.316901],
		[0.362676, -1, -0.221831],
		[0.267606, -1, -0.221831],
		[0.271127, -0.930000, -0.316901],
		[0.362676, -0.930000, -0.316901],
		[0.362676, -0.930000, -0.221831],
		[0.267606, -0.930000, -0.221831],
		
		#AP
		[0.288732, -1, -0.904930],
		[0.397887, -1, -0.904930],
		[0.397887, -1, -0.693662],
		[0.288732, -1, -0.711268],
		[0.288732, -0.930000, -0.904930],
		[0.397887, -0.930000, -0.904930],
		[0.397887, -0.930000, -0.693662],
		[0.288732, -0.930000, -0.711268],
		
		#perpus
		[0.095070, -1, -0.697183],
		[0.225352, -1, -0.704225],
		[0.183099, -1, -0.887324],
		[0.073944, -1, -0.880282],
		[0.095070, -0.930000, -0.697183],
		[0.225352, -0.930000, -0.704225],
		[0.183099, -0.930000, -0.887324],
		[0.073944, -0.930000, -0.880282],
		
		#sunken_atas
		[-0.017606, -0.992, -0.869718],
		[0.024648, -0.992, -0.873239],
		[0.021127, -0.992, -0.757042],
		[-0.021127, -0.992, -0.757042],
		[-0.017606, -1.05, -0.869718],
		[0.024648, -1.05, -0.873239],
		[0.021127, -1.05, -0.757042],
		[-0.021127, -1.05, -0.757042],
		
		#sunken_bawah
		[-0.017606, -0.992, -0.644366],
		[0.010563, -0.992, -0.640845],
		[0.021127, -0.992, -0.725352],
		[-0.021127, -0.992, -0.721831],
		[-0.017606, -1.05, -0.644366],
		[0.010563, -1.05, -0.640845],
		[0.021127, -1.05, -0.725352],
		[-0.021127, -1.05, -0.721831],
		
		# SBM
		[-0.619718, -1, -0.771127],
		[-0.383803, -1, -0.771127],
		[-0.383803, -1, -0.816901],
		[-0.619718, -1, -0.816901],
		[-0.619718, -0.950000, -0.771127],
		[-0.383803, -0.950000, -0.771127],
		[-0.383803, -0.950000, -0.816901],
		[-0.619718, -0.950000, -0.816901],
		
		# CADL
		### GSG kotak berubah jadi CADL persegipanjang
		[-0.285211, -1, -0.637324],
		[-0.197183, -1, -0.637324],
		[-0.197183, -1, -0.859155],
		[-0.285211, -1, -0.859155],
		[-0.285211, -0.950000, -0.637324],
		[-0.197183, -0.950000, -0.637324],
		[-0.197183, -0.950000, -0.859155],
		[-0.285211, -0.950000, -0.859155],
	
		# PAU
		[-0.158451, -1, -0.637324],
		[-0.042254, -1, -0.637324],
		[-0.042254, -1, -0.845070],
		[-0.158451, -1, -0.845070],
		[-0.158451, -0.950000, -0.637324],
		[-0.042254, -0.950000, -0.637324],
		[-0.042254, -0.950000, -0.845070],
		[-0.158451, -0.950000, -0.845070],

		# Menwa
		[-0.612676, -1, -0.711268],
		[-0.383803, -1, -0.711268],
		[-0.383803, -1, -0.746479],
		[-0.612676, -1, -0.746479],
		[-0.612676, -0.950000, -0.711268],
		[-0.383803, -0.950000, -0.711268],
		[-0.383803, -0.950000, -0.746479],
		[-0.612676, -0.950000, -0.746479],

		# labtek 3
		[-0.665493, -1, -0.658451],
		[-0.440141, -1, -0.658451],
		[-0.440141, -1, -0.700704],
		[-0.665493, -1, -0.700704],
		[-0.665493, -0.950000, -0.658451],
		[-0.440141, -0.950000, -0.658451],
		[-0.440141, -0.950000, -0.700704],
		[-0.665493, -0.950000, -0.700704],

		# TI depan
		[-0.616197, -1, -0.566901],
		[-0.482394, -1, -0.566901],
		[-0.482394, -1, -0.612676],
		[-0.616197, -1, -0.612676],
		[-0.616197, -0.950000, -0.566901],
		[-0.482394, -0.950000, -0.566901],
		[-0.482394, -0.950000, -0.612676],
		[-0.616197, -0.950000, -0.612676],
		
		# TI belakang
		[-0.690141, -1, -0.588028],
		[-0.616197, -1, -0.588028],
		[-0.616197, -1, -0.637324],
		[-0.690141, -1, -0.637324],
		[-0.690141, -0.950000, -0.588028],
		[-0.616197, -0.950000, -0.588028],
		[-0.616197, -0.950000, -0.637324],
		[-0.690141, -0.950000, -0.637324],
		
		# lab mesin
		[-0.626761, -1, -0.478873],
		[-0.510563, -1, -0.478873],
		[-0.510563, -1, -0.545775],
		[-0.626761, -1, -0.545775],
		[-0.626761, -0.950000, -0.478873],
		[-0.510563, -0.950000, -0.478873],
		[-0.510563, -0.950000, -0.545775],
		[-0.626761, -0.950000, -0.545775],
				
		##### FUTURE NON-QUADS BUILDING
		# GKU Barat
		#[-0.584507, -1, -0.024648],
		#[-0.454225, -1, -0.024648],
		#[-0.454225, -1, -0.154930],
		#[-0.584507, -1, -0.154930],
		#[-0.584507, -0.950000, -0.024648],
		#[-0.454225, -0.950000, -0.024648],
		#[-0.454225, -0.950000, -0.154930],
		#[-0.584507, -0.950000, -0.154930],
    ]

    texOnly = [
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
    ]

    norOnly = [
        [0, 0, 1],
    ]

    vert = [
        # ALAS
        vertOnly[0] + texOnly[0] + norOnly[0],
        vertOnly[1] + texOnly[1] + norOnly[0],
        vertOnly[2] + texOnly[2] + norOnly[0],
        vertOnly[3] + texOnly[3] + norOnly[0],
    ]

    ind = [
        # use depan texture
        [0, 1, 2, 3],

        #depan belakang
        [4, 5, 9, 8],
        [7, 6, 10, 11],

        #samping
        [5, 6, 10, 9],
        [4, 7, 11, 8],
        #atas
        [8, 9, 10, 11],
    ]

    def makeCuboid(self, startIndex, startNor = 0):
        vert_ans = [
            # depan belakang texture
            self.vertOnly[startIndex + 0] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 1] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 5] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 4] + self.texOnly[3] + self.norOnly[startNor],

            self.vertOnly[startIndex + 3] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 2] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 6] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 7] + self.texOnly[3] + self.norOnly[startNor],

            # samping texture
            self.vertOnly[startIndex + 1] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 2] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 6] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 5] + self.texOnly[3] + self.norOnly[startNor],

            self.vertOnly[startIndex + 0] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 3] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 7] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 4] + self.texOnly[3] + self.norOnly[startNor],

            # atas, texture same with samping 
            self.vertOnly[startIndex + 4] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 5] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 6] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 7] + self.texOnly[3] + self.norOnly[startNor],
        ]
        return vert_ans

    # masukkan base dari bangunan disini
    def initVertices(self):
        jmlCuboid = (len(self.vertOnly) - 4) // 8
        for i in range(0, jmlCuboid):
            self.vert.extend(self.makeCuboid(i*8 + 4))

    #-------------------------------------
    def __init__(self):

        # initialize texture
        self.texEnum = ('jalan','roof','lab7-kirikanan', 'lab7-depanbelakang')
        self.tex = [
            Texture("res/jalan.jpg"),
            Texture("res/roof.jpg"),

            Texture("res/lab7-kanankiri.jpg"),
            Texture("res/lab7-depanbelakang.jpg"),

            Texture("res/gkutimur-kanankiri.jpg"),
            Texture("res/gkutimur-depanbelakang.jpg"),

            Texture("res/doping-kanankiri.jpg"),
            Texture("res/doping-depanbelakang.jpg"),

            Texture("res/geodesi-kanankiri.jpg"),
            Texture("res/geodesi-depanbelakang.jpg"),

            Texture("res/ms-kanankiri.jpg"),
            Texture("res/ms-depanbelakang.jpg"),

            #CC Timur
            Texture("res/cctimur_spg.jpg"),
            Texture("res/cctimur_dpn.jpg"),

            #Altim
            Texture("res/altim_spg.jpg"),
            Texture("res/altim_dpn.jpg"),

            #LFM
            Texture("res/lfm_spg.jpg"),
            Texture("res/lfm_dpn.jpg"),

            #Tekling, HTML
            Texture("res/tekling_spg.jpg"),
            Texture("res/tekling_dpn.jpg"),

            #Labtek IX A
            Texture("res/lab9a_spg.jpg"),
            Texture("res/lab9a_dpn.jpg"),

            #Labtek IX C
            Texture("res/lab9c_spg.jpg"),
            Texture("res/lab9c_dpn.jpg"),

            #Labtek IX B
            Texture("res/lab9b_spg.jpg"),
            Texture("res/lab9b_dpn.jpg"),

            #FSRD
            Texture("res/fsrd_spg.jpg"),
            Texture("res/fsrd_dpn.jpg"),

            #Gedung random pojok kanan bawah
            Texture("res/grpkb_spg.jpg"),
            Texture("res/grpkb_dpn.jpg"),

            #Gedung random pojok kanan bawah
            Texture("res/grpkb2_spg.jpg"),
            Texture("res/grpkb2_dpn.jpg"),

			Texture("res/labmesin-samping.jpg"),
            Texture("res/labmesin-depan.jpg"),
            
            Texture("res/labtekII-samping.jpg"),
            Texture("res/labtekII-depan.jpg"),

            Texture("res/labxi-samping.jpg"),
            Texture("res/labxi-depan.jpg"),

            Texture("res/labtrgm-samping.jpg"),
            Texture("res/labtrgm-depan.jpg"),

            Texture("res/labxi-samping.jpg"),
            Texture("res/labxi-depan.jpg"),
            
            # CRCS
            Texture("res/crcs-samping.jpg"),
            Texture("res/crcs-depan.jpg"),
            
            # Labtek IV
            Texture("res/labtekIV-samping.jpg"),
            Texture("res/labtekIV-depan.jpg"),
            
            # BSC-B
            Texture("res/bsc-b-samping.jpg"),
            Texture("res/bsc-b-depan.jpg"),
            
            # Kimia Atas
            Texture("res/kimia-atas-samping.jpg"),
            Texture("res/kimia-atas-depan.jpg"),
            
            # tvst
            Texture("res/tvst-depanbelakang.jpg"),
			Texture("res/tvst-kirikanan.jpg"),
            
            # oktagon
            Texture("res/oktagon-depanbelakang.jpg"),
            Texture("res/oktagon-kirikanan.jpg"),
            
            # fidas
            Texture("res/fidas-depanbelakang.jpg"),
            Texture("res/fidas-kirikanan.jpg"),
            
            # power
            Texture("res/power-depanbelakang.jpg"), 
            Texture("res/power-kirikanan.jpg"),
            
            # lab 1
            Texture("res/lab1-kirikanan.jpg"),
            Texture("res/lab1-depanbelakang.jpg"),
            
            # lab bahan
            Texture("res/bahan-kirikanan.jpg"),
            Texture("res/bahan-depanbelakang.jpg"),
            
            # AP
            Texture("res/ap-kirikanan.jpg"),
            Texture("res/ap-depanbelakang.jpg"),
            
            # perpus
            Texture("res/perpus-depanbelakang.jpg"),
            Texture("res/perpus-kirikanan.jpg"),
            
            # sunken atas
            Texture("res/sunken-kirikanan.png"),
            Texture("res/sunken-depanbelakang.png"),            
            
            # sunken bawah
            Texture("res/sunken-kirikanan.png"),
            Texture("res/sunken-depanbelakang.png"),
            
            # Kimia Bawah
            Texture("res/kimia-bawah-samping.jpg"),
            Texture("res/kimia-atas-depan.jpg"),
            
            # SBM
            Texture("res/sbm-l.jpg"),
            Texture("res/sbm-p.jpg"),
            
            # CADL
            Texture("res/cadl-l.jpg"),
            Texture("res/cadl-p.jpg"),
            
            # PAU
            Texture("res/pau-p.jpg"),
            Texture("res/pau-l.jpg"),
            
            # Menwa
            Texture("res/menwa-l.jpg"),
            Texture("res/menwa-p.jpg"),
            
            # Labtek 3
            Texture("res/labtek3-l.jpg"),
            Texture("res/labtek3-p.jpg"),
            
            # TI depan
            Texture("res/labtek3-p.jpg"),
            Texture("res/labtek3-p.jpg"),
            
            # TI belakang
            Texture("res/labtek3-p.jpg"),
            Texture("res/labtek3-p.jpg"),
            
            # Lab Mesin
            Texture("res/labmesin-l.jpg"),
            Texture("res/labmesin-p.jpg"),
            
        ]

        # initialize shader
        try:
            self.shader = compileProgram(
                compileShader( VERTEX_SHADER, GL_VERTEX_SHADER ),
                compileShader( FRAGMENT_SHADER, GL_FRAGMENT_SHADER )
            )
        except RuntimeError as err:
            sys.stderr.write( err.args[0] )
            sys.exit( 1 )

        self.initVertices()

        self.vertices = vbo.VBO(np.array(self.vert, dtype='f'))
        self.indices = vbo.VBO(np.array(self.ind, dtype='uint32'),target='GL_ELEMENT_ARRAY_BUFFER')

        for uniform in (
            'Global_ambient',
            'Light_ambient',
            'Light_diffuse',
            'Light_location',
            'Material_ambient',
            'Material_diffuse',
        ):
            location = glGetUniformLocation( self.shader, uniform )
            if location in ( None, -1 ):
                print ('Warning, no uniform: %s'%( uniform ))
            setattr( self, uniform+ '_loc', location )

        for attribute in (
            'Vertex_position',
            'Vertex_texCoord',
            'Vertex_normal',
        ):
            location = glGetAttribLocation(self.shader, attribute)
            if location in ( None, -1 ):
                print ('Warning, no attribute: %s' %( attribute ))
            setattr( self, attribute + '_loc', location )

    def initMesh(self):
        glUniform4f( self.Global_ambient_loc, .9,.05,.05,.1 )
        glUniform4f( self.Light_ambient_loc, .2,.2,.2, 1.0 )
        glUniform4f( self.Light_diffuse_loc, 1,1,1,1 )

        glUniform3f( self.Light_location_loc, 2,2,10 )
        glUniform4f( self.Material_ambient_loc, .2,.2,.2, 1.0 )
        glUniform4f( self.Material_diffuse_loc, 1,1,1, 1 )

        stride = 8*4 # x y z x_tex y_tex r g b * sizeof(float)
        glEnableVertexAttribArray( self.Vertex_position_loc ) # 0
        glEnableVertexAttribArray( self.Vertex_texCoord_loc ) # 1
        glEnableVertexAttribArray( self.Vertex_normal_loc ) # 2

        # bind the vertex attribute location
        glVertexAttribPointer(self.Vertex_position_loc, 3, GL_FLOAT, False, stride, self.vertices)
        glVertexAttribPointer(self.Vertex_texCoord_loc, 2, GL_FLOAT, False, stride, self.vertices + 12)
        glVertexAttribPointer(self.Vertex_normal_loc  , 3, GL_FLOAT, False, stride, self.vertices + 20)

    def draw(self):
        '''
        render the scene geometry
        '''
        glUseProgram(self.shader)

        try:
            self.vertices.bind()
            self.indices.bind()
            try:
                self.initMesh()

                self.tex[0].Bind(0)
                glDrawArrays(GL_QUADS, 0, 4)
                #glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, ctypes.c_void_p(0))

                cuboid_count = (self.vert.__len__() - 4) // 20


                #khusus labtek tengah texture sama
                for i in range(0, 5):
                    self.tex[3].Bind(0) #depan belakang
                    glDrawArrays(GL_QUADS, i * 20 + 4, 8)
                   
                    self.tex[2].Bind(0) #kanan kiri
                    glDrawArrays(GL_QUADS, i * 20 + 12, 8)

                    self.tex[1].Bind(0) #atap
                    glDrawArrays(GL_QUADS, i * 20 + 20, 4)

                #bangunan berikutnya
                for i in range(5, cuboid_count):
                    self.tex[(i-4)*2 + 1].Bind(0) #depan belakang
                    glDrawArrays(GL_QUADS, i * 20 + 4, 8)

                    self.tex[(i-4)*2].Bind(0) #kanan kiri
                    glDrawArrays(GL_QUADS, i * 20 + 12, 8)

                    self.tex[1].Bind(0) #atap
                    glDrawArrays(GL_QUADS, i * 20 + 20, 4)

            finally:
                self.vertices.unbind()
                self.indices.unbind()

                glDisableVertexAttribArray( self.Vertex_position_loc ) # 0
                glDisableVertexAttribArray( self.Vertex_texCoord_loc ) # 1
                glDisableVertexAttribArray( self.Vertex_normal_loc ) # 2
        finally:
            glUseProgram(0)

    def render_scene(self):
        Display.Clear()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        global ry, rx, tx, ty, zpos
        glTranslatef(tx/20., ty/20., - zpos)
        glRotated(ry, 1, 0, 0)
        glRotated(rx, 0, 1, 0)
        #  glTranslatef(0, 1,-60)
        #glRotatef(30,30,60,0)
        #  glRotatef(self.y_axis,0,1,0)
        
        self.draw()

        self.y_axis = self.y_axis - 1

def main():
    pygame.init()
    pygame.display.set_mode((WIDTH , HEIGHT),pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("petaITB")
    clock = pygame.time.Clock()
    done = False

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluPerspective(2, 1.0 * WIDTH/HEIGHT, 0.01, 1000.0)
    
    gluPerspective(30, 1.0 * WIDTH/HEIGHT, 0.001, 500.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    petaitb = petaITB()
    global rx, ry, ty, tx, zpos
    
    rotate = move = pressed = False
    into = 'A'
    #----------- Main Program Loop -------------------------------------
    while not done:
        # --- Main event loop
        if into =='o' and pressed:
             zpos += 1
        elif into =='i' and pressed:
             zpos = max(1, zpos-1)
        elif into =='q' and pressed:
             rx -= 1
        elif into =='e' and pressed:
             rx += 1
        elif into =='w' and pressed:
             ty -= 1
        elif into =='s' and pressed:
             ty += 1
        elif into =='a' and pressed:
             tx += 1
        elif into =='d' and pressed:
             tx -= 1
        elif into =='r' and pressed:
             ry += 1
        elif into =='f' and pressed:
             ry -= 1        			
        for e in pygame.event.get(): # User did something
            if e.type == KEYUP:
                pressed = False
            if e.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4: zpos = max(1, zpos-1)
                elif e.button == 5: zpos += 1
                elif e.button == 1: rotate = True
                elif e.button == 3: move = True
            elif e.type == KEYDOWN and e.key == K_o:
                zpos += 1
                into = 'o'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_i:
                zpos = max(1, zpos-1)
                into = 'i'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_q:
                rx -= 1
                into = 'q'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_r:
                ry += 1
                into = 'r'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_f:
                ry -= 1
                into = 'f'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_e:
                rx += 1
                into = 'e'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_a:
                tx += 1
                into = 'a'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_d:
                tx -= 1
                into = 'd'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_w:
                ty -=1
                into = 'w'
                pressed = True
            elif e.type == KEYDOWN and e.key == K_s:
                ty += 1
                into = 's'
                pressed = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1: rotate = False
                elif e.button == 3: move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j
        clock.tick(30)
        
        # RENDER OBJECT
        petaitb.render_scene()
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()
