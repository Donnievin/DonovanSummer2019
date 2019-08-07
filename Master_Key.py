#import all the good stuff!
#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import pynbody
import pylab
import numpy as np
import matplotlib.pylab as plt
import readcol

'''
r = (G * BH_Mass) / (stars_vel**2)
G = 6.674e-11
'''

#Now I need a code that will load the snapshots(s will stand for )
Path = "/media/jillian//cptmarvel/cptmarvel.cosmo25cmb.4096g5HbwK1BH.004096/supersample/highres/"
files = readcol.readcol('/media/jillian/cptmarvel/cptmarvel.cosmo25cmb.4096g5HbwK1BH.004096/supersample/highres/files.list')
all_files = files[:,0]

#Tell where BH is Function
def findBH(s):
    BH = s.stars[pynbody.filt.LowPass('tform', 0.0)]
    return BH

#std stands for standard deviation (velocity dispersion)
def DispersionVelocity(s):
    velocity = s.stars['vel']
    x = np.std(velocity[0])
    y = np.std(velocity[1])
    z = np.std(velocity[2])
    #print(x_direct)
    #print(y_direct)
    #print(z_direct)
    dispersion_velocity = np.sqrt( (x)**2 + (y)**2 + (z)**2)
    #print(dispersion_velocity)
    return dispersion_velocity

#Need my units to match up so the calculations go correctly
#Couldn't find a way to convert G, so i converted everything else and then converte back to KPC
def RadInfluence(s):
    G = 6.674e-11
    #G is in m**3 * kg**-1 * s**-2
    BH = findBH(s)
    BH_Mass = BH['mass'].in_units('kg')
    #Kg mtches kg in G
    stars_vel = DispersionVelocity(s) * 1e3
    r = (G * BH_Mass) / (stars_vel**2)
    return r * 3.24e-20
#Finally converted back to KPC (the conversion is * 3.24e-20)

def StarPosition(s):
    stars_pos = s.stars['pos']
    posx = stars_pos[:,0]
    posy = stars_pos[:,1]
    posz = stars_pos[:,2]
    position = np.sqrt((posx)**2 + (posy)**2 + (posz)**2)
    return position

#This line of code is going to create a txt called LoopData
f= open("RadInfluence.txt","w+")
f.write("BH Position, BH Velocity, Star Vel(Sphere),BH Mass")
#It adds everything in the for loop



#Pt1 BH, Pt2 Sphere, Pt3 Sphere Properties
for i in all_files:
    s = pynbody.load(Path + i)
    s.physical_units()
    #Don't forget to center the galaxy with this
    pynbody.analysis.angmom.faceon(s)
    BH = findBH(s)
    Mass_Msol = BH['mass']
    #print(Mass_Msol)
    BH_pos = BH['pos']
    BHx = BH_pos[:,0]
    BHy = BH_pos[:,1]
    BHz = BH_pos[:,2]
    #This solves for the blackholes position
    BH_POSITION = np.sqrt((BHx)**2 + (BHy)**2 +(BHz)**2)
    #This keeps the BH position as a 3 len array
    BH_position = np.array([BHx[0], BHy[0], BHz[0]])
    #print(type(BH_POSITION))
    BH_vel = BH['vel']
    BH_velx = BH_vel[:,0]
    BH_vely = BH_vel[:,1]
    BH_velz = BH_vel[:,2]
    BH_velocity = np.array((BH_velx)**2 + (BH_vely)**2 + (BH_velz)**2)

    
    #We need the radius to be an integer
    radius = RadInfluence(s)
    radius_influence = radius[0] * 3
    #print(radius)
    #BH_pos is a three int array so it will be the center
    sphere = pynbody.filt.Sphere(radius_influence, cen = BH_position)
    #print(sphere)
    
    stars = s.stars[0:]
    #print(len(stars))
    stellar_mass = s.stars['mass'].sum()
    #print()
    in_sphere = stars[sphere]
    total_stars = len(in_sphere)
    #print(total_stars)
    in_sphere_vel = in_sphere['vel']
    star_velx = in_sphere_vel[:,0]
    star_vely = in_sphere_vel[:,1]
    star_velz = in_sphere_vel[:,2]
    star_velocity = np.sqrt((star_velx)**2 + (star_vely)**2 + (star_velz)**2)

    Sphere_no_BH = star_velocity - BH_velocity
    data = str(BH_POSITION)+"   "+str(BH_velocity[0])+"   "+str(star_velocity[0])+"   "+str(Mass_Msol[0])
    f.write(data+'\n')
f.close()
'''
    #This will give the position of every star in the sphere
    in_sphere_pos = in_sphere['pos']
    posx = in_sphere[:,0]
    posy = in_sphere[:,1]
    posz = in_sphere[:,2]
    position = np.sqrt((posx)**2 + (posy)**2 + (posz)**2)
    #print(position)
    #This will sort every star in order by distance
    star_distance = np.sort(position)
    #print(star_distance)
'''
    
'''
    data = str("BH_POSITION"+"   "+"BH_velocity"+"   "+"Star_velocity"+"   "+"Sphere_no_BH"+"\n")
    data = str(data)
    data = data[1:-1]
    f.write(data+'\n')
    print(data)

f.close()
'''
