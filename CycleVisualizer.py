# Takes cycle data and generates graph to help visualize cycle lengths
# Created 8/6/20
# Written by Justin Yu

import sys

waterFILE = sys.argv[1]
sugarFILE = sys.argv[2]

water = open(waterFILE, "r")
sugar = open(sugarFILE, "r")

print("sugar:" + sugar.read())
print("water:" + water.read())

