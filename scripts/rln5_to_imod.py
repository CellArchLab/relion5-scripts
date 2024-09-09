#!/usr/bin/env python

import argparse
import starfile
import sys
import os
import numpy as np
import subprocess

def parse_args():
		
	parser = argparse.ArgumentParser(description="Randomize half-sets based on odd/even order of particles.")
	parser.add_argument("--instar", type=str, help="Path to input RELION-5 STAR file.")
	parser.add_argument("--outmod", type=str, help="Path to output IMOD model file.")
	parser.add_argument("--tomo", type=str, help="Name of tomogram for visualization.")
	parser.add_argument("--angpix", type=float, help="Pixel size of the tomogram for visualization.")
	parser.add_argument("--x", type=float, help="X dimension of tomogram for visualization.")
	parser.add_argument("--y", type=float, help="Y dimension of tomogram for visualization.")
	parser.add_argument("--z", type=float, help="Z dimension of tomogram for visualization.")
		
	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	return parser.parse_args()

def main():

	args = parse_args()

	instar = args.instar
	outmod = args.outmod
	outtxt = os.path.splitext(outmod)[0] + '.txt'
	tomo = args.tomo
	x = args.x
	y = args.y
	z = args.z
	apix = args.angpix

	rln = starfile.read( instar )
		
	sel = rln['particles']['rlnTomoName'] == tomo

	xyz_centered_ang = np.array( [ rln['particles'].loc[sel, 'rlnCenteredCoordinateXAngst'], rln['particles'].loc[sel, 'rlnCenteredCoordinateYAngst'], rln['particles'].loc[sel, 'rlnCenteredCoordinateZAngst'] ] )
	# print(xyz_centered_ang.shape)

	if 'rlnOriginZAngst' in rln['particles'].keys():
		xyz_centered_ang -= np.array( [ rln['particles'].loc[sel, 'rlnOriginXAngst'], rln['particles'].loc[sel, 'rlnOriginYAngst'], rln['particles'].loc[sel, 'rlnOriginZAngst'] ] )

	xyz_centered = np.transpose(xyz_centered_ang) / apix
	xyz = xyz_centered
	xyz[:,0] += x / 2
	xyz[:,1] += y / 2
	xyz[:,2] += z / 2

	# Save the array to a text file (e.g., 'output.txt')
	np.savetxt(outtxt, xyz, fmt='%.2f', delimiter='  ')
	command = "point2model -scat -sphere 10 -pixel %.3f,%.3f,%.3f %s %s" % (apix, apix, apix, outtxt, outmod) 
	subprocess.run(command, shell = True, executable="/bin/bash")
		
if __name__ == "__main__":
	main()