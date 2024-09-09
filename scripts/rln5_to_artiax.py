#!/usr/bin/env python

import argparse
import starfile
import sys
import numpy as np

def parse_args():
		
	parser = argparse.ArgumentParser(description="Make RELION-5 STAR files compatible with ArtiaX.")
	parser.add_argument("--instar", type=str, help="Path to input RELION-5 STAR file.")
	parser.add_argument("--outstar", type=str, help="Path to output RELION-5 STAR file.")
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
	outstar = args.outstar
	x = args.x
	y = args.y
	z = args.z

	rln = starfile.read( instar )
	rln['particles']['rlnTomoNameOriginal'] = ""
	for idx,tomo in enumerate( np.unique( rln['particles']['rlnTomoName'] ) ):
		
		sel = rln['particles']['rlnTomoName'] == tomo
		rln['particles'].loc[sel, 'rlnTomoNameOriginal'] = tomo
		rln['particles'].loc[sel, 'rlnTomoName'] = f"tomo_{idx+1:04}"

	rln['particles']['rlnCoordinateX'] = rln['particles']['rlnCenteredCoordinateXAngst'] / rln['particles']['rlnDetectorPixelSize'] + x / 2
	rln['particles']['rlnCoordinateY'] = rln['particles']['rlnCenteredCoordinateYAngst'] / rln['particles']['rlnDetectorPixelSize'] + y / 2
	rln['particles']['rlnCoordinateZ'] = rln['particles']['rlnCenteredCoordinateZAngst'] / rln['particles']['rlnDetectorPixelSize'] + z / 2

	starfile.write( rln, outstar, overwrite=True) 
		
if __name__ == "__main__":
	main()