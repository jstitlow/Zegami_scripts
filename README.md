# Zegami_scripts

## SUMMARY OF WORKFLOW TO BUILD ZEGAMI COLLECTION

1. Clone the repository and cd into it. 

    `git clone 

1. Begin OMERO session by typing the following command into the command line.
    
    `make login`

2. Generate zegami.csv file from OMERO.Figure names that include Zegami.
    
    `python list-figures.py`
    
3. Download figures as json files.
    
    `python download-figures.py /path/to/outdir /path/to/zegami.csv`
    
    * will have to delete first row because the code is looking integer values

4. Convert json files to jpg for the scoring app

    `python figure-json2jpeg.py /path/to/outdir /path/to/zegami.csv`

5. Convert .jpg files to .png for Zegami. 

    `python convert_jpg2png.py`
    
6. Add other datasets to zegami.csv file

    `python run runFlymineQueries_zegami.py #needs Py2 because of some dictionary nonsense
    
      -export PATH="/usr/people/bioc1301/miniconda3/bin:$PATH"
      
      -source activate py27

## TO DO:

* write code to merge other datasets to the zegami text file

    -Davis lab sequencing data
    -Other sources
    -flymine output
    -smFISH screen annotations

## KNOWN ISSUES:
* zegami.csv has to be cleaned up as follows
    * remove Maria's data and others that are mis-labelled
    -remove template data
    -remove hyphens from CPTI ID numbers
    -several typos in figure_name (CPTI numbers) that make it difficult to correlate

SUMMARY OF WORKFLOW TO USE SCORING APP
-Generate image files (.jpgs) and ID table using the Zegami workflow above
-Run questionnaire.py script
    -arguments
        -questions path
        -answers dir
        -image path
        
20181015
Cleaning up the code for generating Zegami databases
-list-figures.py find all of the figures in Omero labelled Zegami and parse the filenames into a .csv file
 just as the figure2zegami.py script does
