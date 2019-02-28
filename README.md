# Zegami_scripts

## SUMMARY OF WORKFLOW TO BUILD ZEGAMI COLLECTION

1. Clone the repository and cd into it. 

    `git clone https://github.com/jstitlow/Zegami_scripts`
    
    `cd Zegami_scripts`
    
2. Add environmental variables for omero and PYTHONPATH to your bash profile

    `nano ~/.bash_profile`
    
    * export OMERO="/opt/OMERO.py-5.4.8-ice36-b99/bin/omero"
    
    * export PYTHONPATH="/opt/OMERO.py-5.4.8-ice36-b99/lib/python/:$PYTHONPATH"
    
    * control + x; y

3. Begin OMERO session by typing the following command into the command line.
    
    `make login`

4. Generate zegami.csv file from OMERO.Figure names that include Zegami.
    
    `python list-figures.py`
    
5. Download figures as json files.
    
    `python download-figures.py /path/to/outdir /path/to/zegami.csv`
    
    * will have to delete first row because the code is looking integer values

6. Convert json files to jpg for the scoring app

    `python figure-json2jpeg.py /path/to/outdir /path/to/zegami.csv`

7. Convert .jpg files to .png for Zegami. 

    `python convert_jpg2png.py`
    
8. Populate the zegami.csv file with datasets from Intermine, Davis lab, and the literature

    `python run runFlymineQueries_zegami.py -outname -infile -query_dir -dataset_dir`
    
    * can add additional data by adding .csv file to dataset_dir with FBgn's in 1st column for indexing
    
    * needs Py2 because of some dictionary nonsense
    
    * export PATH="/usr/people/bioc1301/miniconda3/bin:$PATH"
      
    * source activate py27

## TO DO:

* merge the scripts

* fix dictionary issue in runFlymineQueries_zegami.py

## KNOWN ISSUES:

    ### zegami.csv has to be cleaned up as follows

        * remove Maria's data and others that are mis-labelled
        * remove template data
        * remove hyphens from CPTI ID numbers
        * several typos in figure_name (CPTI numbers) that make it difficult to correlate

## SUMMARY OF WORKFLOW TO USE SCORING APP

1. Generate image files (.jpgs) and ID table using the Zegami workflow above

2. Run questionnaire.py script

    `python questionnaire.py /path/to/questions/file /path/to/answers/dir /path/to/image/dir`
        
