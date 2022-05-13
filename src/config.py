" Module that defines variables for program"

##############
# File Paths #
##############

# defined by USER
instructionsName = "Instructions - calcSLD.txt"
inputDir  = "../../UoM-Data-Repository/input/" + instructionsName
outputDir = "../../UoM-Data-Repository/output/calcSLD"


#################
# Print Options #
#################

# determine levels of print output to terminal for debugging
verbose      = False
very_verbose = False


##############
# Parameters #
##############

# Get analysis parameters from input instructions
import csv, ast
with open(inputDir, newline = '') as f:
    fileList            = list(csv.reader(f))
    compactChains       = ast.literal_eval(fileList[0][1].split('=')[1])
    addLipidToMonolayer = ast.literal_eval(fileList[0][2].split('=')[1])
    addDrugToThirdLayer = ast.literal_eval(fileList[0][3].split('=')[1])
    addDrugToMonolayer  = ast.literal_eval(fileList[0][4].split('=')[1])


## Multiply average chain vol by factor to model lipid chain compaction
chainCompactFactor = 0.85

## Add injected lipid into the existing monolayer
injectedLipidNames       = ["Monolayer", "DMG-PEG-2000"] # "DLin-MC3-DMA" "DMG-PEG-2000"
injectedLipidRatios      = [99, 1]
updateMonolayerThickness = False
new_d1 = 0
new_d2 = 0

## Adding injected drug to system
injectedDrugNames   = ["PolyA","PEG"] # "PolyA", "PEG"
injectedDrugRatios  = [99,1]
injectedDrugSizes   = [20, 0]
injectedDrugSLD_H2O = {"PolyA": 3.67, "PEG": 0.62}
injectedDrugSLD_D2O = {"PolyA": 4.46, "PEG": 0.62}
threeSolv           = 86.75

## Use contentious vol frac (True) or default molar ratio (False)
useVolFrac = False


##############
# Databases #
#############

# atom coherent scattering lengths [fm], Coh b from https://www.ncnr.nist.gov/resources/n-lengths/
atomSL = {
    "H": -3.739,
    "D": 6.671,
    "C": 6.646,
    "N": 9.36,
    "O": 5.803,
    "P": 5.13,
    "K": 3.67,
    }

# molecular weight lipid database, [g/mol]
lipidMw = {
    "DPPC":            734.039,
    "d-DPPC":          796.43,
    "POPC":            760.07,  # 760.076
    "d31-POPC":        791.07,  # 791.267
    "POPS":            783.99,
    "Cholesterol":     386.65,  # 386.654
    "d45-Cholesterol": 432,
    "DLin-KC2-DMA":    642.1,
    "DLin-MC3-DMA":    642.09,
    "d62-DLin-MC3-DMA":704.5,
    "DOPE":            744.034,
    "SM":              760.223,
    "LBPA":            792.07,
    "PolyA":           385.31,
    "DMG-PEG-2000":    2509.200,
    }

# chemical structures for each lipid: (struct_head, struct_tail)
lipidStruct = {
    "POPC":            ('N-O8-P-C10-H18', 'C32-H64'), # Yixuan struct. email 03-04-22
    "d31-POPC":        ('N-O8-P-C10-H18', 'C32-D31-H33'),
    "DOPE":            ('N-O8-P-C8-H14', 'C33-H64'),
    "SM":              ('N2-O5-P-C8-H19', 'O1-C33-H64'),
    "LBPA":            ('N-O4-P-C4-H11', 'O6-C38-H71'),
    "Cholesterol":     ('O-H','C27-H45'),
    "d45-Cholesterol": ('O-H','C27-D45'),
    "DLin-MC3-DMA":    ('N-O2-C7-H13', 'C36-H66'),
    "d62-DLin-MC3-DMA":('N-O2-C7-H13', 'C36-H4-D62'),
    "DSPC":            ('N-O8-P-C10-H18','C34-H70'),
    "d70-DSPC":        ('N-O8-P-C10-H18','C34-D70'),
    "DMG-PEG-2000":    ('O5-C6-H7','C25-H52'), # polymer: ([O-C2-H4]_44 + O-C3-H7); total: O50-C122-H242
    "PolyA":           ('C10-H13-K-N5-O7-P','H'),
    }

# molecular volumes for each lipid (Angstroms cubed): (head, tail)
lipidMolVol = {
    "POPC":            (344,937),
    "d31-POPC":        (344,937),
    "DOPE":            (236,969),
    "SM":              (274,953),
    "LBPA":            (208,624),
    "Cholesterol":     (5,624),
    "d45-Cholesterol": (5,624),
    "DLin-MC3-DMA":    (260, 1030),
    "d62-DLin-MC3-DMA":(260, 1030),
    "DSPC":            (322,1000),
    "d70-DSPC":        (322,1000),
    "DMG-PEG-2000":    (256,767), # From Marianna: DMPE (head 0.25% total vol. 1023) PEG unit = 670
    "PolyA":           (1,1),
    }
