# Gaussian Cube files loader
# http://erg.biophys.msu.ru/wordpress/archives/150
# Author: Peter Mamonov

import numpy as np
from math import ceil, floor, sqrt

class CUBE:
    def __init__(self, fname):
        f = open(fname, 'r')
        for i in range(2): f.readline() # echo comment
        tkns = f.readline().split() # number of atoms included in the file followed by the position of the origin of the volumetric data
        self.natoms = int(tkns[0])
        self.origin = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
# The next three lines give the number of voxels along each axis (x, y, z) followed by the axis vector.
        tkns = f.readline().split() #
        self.NX = int(tkns[0])
        self.X = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
        tkns = f.readline().split() #
        self.NY = int(tkns[0])
        self.Y = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
        tkns = f.readline().split() #
        self.NZ = int(tkns[0])
        self.Z = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
# The last section in the header is one line for each atom consisting of 5 numbers, the first is the atom number, second (?), the last three are the x,y,z coordinates of the atom center. 
        self.atoms = []
        for i in range(self.natoms):
            tkns = f.readline().split()
            self.atoms.append([tkns[0], tkns[2], tkns[3], tkns[4]])
# Volumetric data
        self.data = np.zeros((self.NX,self.NY,self.NZ))
        i=0
        for s in f:
            for v in s.split():
                self.data[int(i/(self.NY*self.NZ)), int((i/self.NZ)%self.NY), i%self.NZ] = float(v)
                i+=1
        if i != self.NX*self.NY*self.NZ: raise NameError("FSCK!")
     
    def dump(self, f):
# output Gaussian cube into file descriptor "f". 
# Usage pattern: f=open('filename.cube'); cube.dump(f); f.close()
        print("CUBE file\ngenerated by piton _at_ erg.biophys.msu.ru", file=f)
        print("%4d %.6f %.6f %.6f" % (self.natoms, self.origin[0], self.origin[1], self.origin[2]), file=f)
        print("%4d %.6f %.6f %.6f"% (self.NX, self.X[0], self.X[1], self.X[2]), file=f)
        print("%4d %.6f %.6f %.6f"% (self.NY, self.Y[0], self.Y[1], self.Y[2]), file=f)
        print("%4d %.6f %.6f %.6f"% (self.NZ, self.Z[0], self.Z[1], self.Z[2]), file=f)
        for atom in self.atoms:
            print("%s %d %s %s %s" % (atom[0], 0, atom[1], atom[2], atom[3]), file=f)
        for ix in range(self.NX):
            for iy in range(self.NY):
                 for iz in range(self.NZ):
                        print("%.5e " % self.data[ix,iy,iz], end=' ', file=f)
                        if (iz % 6 == 5): print('', file=f)
                 print("", file=f)
 
    def mask_sphere(self, R, Cx,Cy,Cz):
# produce spheric volume mask with radius R and center @ [Cx,Cy,Cz]
# can be used for integration over spherical part of the volume
        m=0*self.data
        for ix in range( int(ceil((Cx-R)/self.X[0])), int(floor((Cx+R)/self.X[0])) ):
            ryz=sqrt(R**2-(ix*self.X[0]-Cx)**2)
            for iy in range( int(ceil((Cy-ryz)/self.Y[1])), int(floor((Cy+ryz)/self.Y[1])) ):
                    rz=sqrt(ryz**2 - (iy*self.Y[1]-Cy)**2)
                    for iz in range( int(ceil((Cz-rz)/self.Z[2])), int(floor((Cz+rz)/self.Z[2])) ):
                            m[ix,iy,iz]=1
        return m



bohr2angs = lambda x: round(0.529177*x, 6)
bohr2angstrom = np.vectorize(bohr2angs)

def cube2angstrom(data):
    """ Correct way of converting Bohr unit in CUBE format to Angstrom """
    if data.X[0] > 0:
        X = bohr2angstrom(data.X)
        Y = bohr2angstrom(data.Y)
        Z = bohr2angstrom(data.Z)
        origin = bohr2angstrom(data.origin)
    else:
        X = data.X
        Y = data.Y
        Z = data.Z
        origin = data.origin

    x_step = np.linalg.norm(X)
    y_step = np.linalg.norm(Y)
    z_step = np.linalg.norm(Z)
    return origin, x_step, y_step, z_step
