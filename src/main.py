" calcSLD "
" Author: @S.Winnall "

# general imports
import glob, os, sys
import pandas as pd
import csv
import shutil
from shutil import copyfile

# import program files
import config
import calculations


# general function importing files
def getFile(path,nSkip,delim):
    return pd.read_csv(path, skiprows=nSkip, sep=delim, comment='#', na_values =' ', skip_blank_lines=True, encoding = "utf-8") # on_bad_lines='skip',


def organisePaths():

    # get instructions name
    instructionsName = config.instructionsName

    # root inputParams file path/directory
    inputFileDir  = config.inputDir

    # root output directory
    outputFolderDir = config.outputDir

    # get analysis title
    with open(inputFileDir, newline = '') as f:
        title = list(csv.reader(f))[0][0].split('=')[1]

    # read instructions file with pandas
    instructionsFile = getFile(path=inputFileDir,nSkip=1,delim=',')

    # update output path folder dir to include title of chosen analysis
    # e.g. output/analysisTitle/
    outputDataPath = '' + outputFolderDir + '/' + title + ''

    try:
        # delete folder if exists and create it again
        shutil.rmtree(outputDataPath)
        os.mkdir(outputDataPath)
    except FileNotFoundError:
        os.mkdir(outputDataPath)

    try:
        # copy input instructions instructionsFilermation to outputDataPath directory
        shutil.copyfile(inputFileDir, outputDataPath + '/' + instructionsName + '.txt')

        # rename copied instructions file to include analysis title
        # this is the file which will be appended in the relevant analysis
        old_name              = outputDataPath + '/' + instructionsName + '.txt'
        outputInstructionFile = outputDataPath + '/' + title + ' - ' + instructionsName + '.txt'
        os.rename(old_name, outputInstructionFile)


    # if source and destination are same
    except shutil.SameFileError:
        print("Instructions Copying Error:\n  Source and destination represents the same file.")

    # if destination is a directory
    except IsADirectoryError:
        print("Instructions Copying Error:\n  Destination is a directory.")

    # if there is any permission issue
    except PermissionError:
        print("Instructions Copying Error:\n  Permission denied.")

    # other errors
    except:
        print("Instructions Copying Error:\n  Error occurred while copying file.")


    # clean output file by getting file (auto skips commented lines)
    File = getFile(path=outputInstructionFile,nSkip=0,delim=',')

    # write new file without the comments (isolates just the files that were run)
    File.to_csv(outputInstructionFile)

    return instructionsFile, title, outputDataPath, outputInstructionFile




def main():

    calcSLD = True
    while calcSLD:

        # reads instructions instructionsFile, gets title and paths
        instructionsFile, title, outputDataPath, outputInstructionFile = organisePaths()

        calculations.main(instructionsFile, outputInstructionFile)

    return


if __name__ == '__main__':
    print("\n\nLaunching...")
    print("\nAuthor: Samuel Winnall \nEmail:  winnall@ill.fr\n")

    main()
