#############################################################################
# OMERO_Figure_to_Zegami.property
#
# Creates .jpg from OMERO.Figures based on identifiers in the Figure FileName
#
# --Usage--
#
# 1) Edit the BlitzGateway details below (one time only!)
#
# 2) Edit the outdir below
#
# 3) Call the script like this:
#     >python OMERO_Figure_to_Zegami.py
#
# --TO DO--
#
# 1) Integrate runFlymineQueries_zegami.py script
#
# 2) Find/fix bug in this bit of code:
#    -            fig_export = TiffExport(conn, export_params,
#                                export_images=False)
#
#############################################################################


import omero
from omero.gateway import BlitzGateway
import csv
import json
import os
import sys
import getpass
import pandas as pd
from Figure_To_Pdf import TiffExport
from PIL import Image
import logging

# Specify output directory
outdir = ('/usr/people/bioc1301/src/Zegami_scripts/Zegami_collection_May_2019')
zegami_csv = ('zegami.csv')
logging.basicConfig(filename='zegami.log',level=logging.DEBUG)

# Initialise OMERO
PASS = getpass.getpass("Enter Password:")
conn = BlitzGateway('bioc1301', PASS,
        host='omero1.bioch.ox.ac.uk', port=4064, group='davisgroup')
conn.connect()
conn.SERVICE_OPTS.setOmeroGroup(-1)

# create a list of OMERO.FigureIDs in .csv file
def list_figures():
    y = open(zegami_csv,'w')
    z = csv.writer(y)
    z.writerow(["figure_id","Gene","Collection", "Compartment","Probe"])

    for fig in conn.getObjects('FileAnnotation',
            attributes={'ns': 'omero.web.figure.json'}):
        filename = fig.getFileName()
        if 'zegami1' not in filename and 'zegami2' not in filename:
            continue
        fig_metadata = filename.split('_')
        figure_id = ('%d' % (fig.getId()))
        Gene = ('%s' % (fig_metadata[0]))
        Collection = ('%s' % (fig_metadata[1]))
        Compartment = ('%s' % (fig_metadata[2]))
        Probe = ('%s' % (fig_metadata[3]))
        min_info = figure_id,Gene,Collection,Compartment,Probe
        print ('extracting:', min_info)
        logging.debug(('extracting:', min_info))
        z.writerow(min_info)

# download OMEROfigure json files and build jpgs
def figure_json_to_jpg():

    # get OMERO.FigureIDs
    figure_IDs = pd.read_csv(zegami_csv, header=0)
    figure_IDs = figure_IDs['figure_id']

    for fig_ID in figure_IDs:
        try:
            # find .json text from the Figure
            fig = conn.getObject('FileAnnotation', fig_ID)
            if fig is None:
                print fig_ID, 'is broken'
                logging.debug((fig_ID, 'is broken'))

            try:
                # get .json text from the Figure and write .json file
                fig_json = json.loads("".join(fig.getFileInChunks()))
                with open(os.path.join(outdir, str(fig_ID)+'.json'), 'w') as fh:
                    json.dump(fig_json, fh)
                    print ('downloaded figure:', fig_ID)
                    logging.debug(('downloaded figure:', fig_ID))
            except:
                print (fig_ID, 'does not exist')
                logging.debug((fig_ID, 'does not exist'))
                continue
        except:
            pass

        # open .json file
        json_path = os.path.join(outdir, str(fig_ID)+'.json')
        with open(json_path, 'r') as fh:
            fig_text = fh.read()

        # build jpg file
        fig_json = json.loads(fig_text)
        try:
            if int(fig_json['page_count']) > 1:
                raise RuntimeError("more than one page for figure id '%d'" % fig_id)
        except:
            pass
        export_params = {
            'Figure_JSON' : fig_text,
            'Webclient_URI': 'https://omero1.bioch.ox.ac.uk',
            'Export_Option' : 'TIFF', # change to jpeg
        }
        try:
            fig_export = TiffExport(conn, export_params,
                                export_images=False)
        except:
            print (fig_ID, 'has attribute error')
            continue
        def get_figure_file_name(page=None):
            return os.path.join(outdir, str(fig_ID)+'.jpg')
        fig_export.get_figure_file_name = get_figure_file_name

        try:
            fig_export.build_figure()
            print ('built:', str(fig_ID)+'.jpg')
            logging.debug(('built:', str(fig_ID)+'.jpg'))

        except:
            print("failed to build figure",str(fig_ID)+'.jpg')
            logging.debug(("failed to build figure",str(fig_ID)+'.jpg'))

def convert_jpg_to_png():
    jpg_files = os.listdir(outdir)
    for jpg in jpg_files:
        if jpg.endswith('.jpg'):
            im = Image.open(os.path.join(outdir, jpg))
            im.save(os.path.join(outdir, jpg.replace('.jpg','.png')))
            print ('converted ', jpg, 'to .png')
            logging.debug(('converted ', jpg, 'to .png'))

list_figures()
#figure_json_to_jpg()
#convert_jpg_to_png()

conn.close
