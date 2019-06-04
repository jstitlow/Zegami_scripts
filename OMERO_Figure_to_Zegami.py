#############################################################################
# OMERO_Figure_to_Zegami.property
#
# Creates .jpg from OMERO.Figures based on identifiers in the Figure FileName
#
# --Usage--
# 1) Login to OMERO CLI like this:
#     >omero login
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
#############################################################################

import omero_tools
import csv
import json
import os
import sys
import omero
import pandas as pd
from Figure_To_Pdf import TiffExport
from PIL import Image

# Specify output directory
outdir = ('/usr/people/bioc1301/src/Zegami_scripts/Zegami_collection_May_2019')
zegami_csv = ('zegami.csv')

# Initialise OMERO
conn = omero_tools.get_connection()
conn.SERVICE_OPTS.setOmeroGroup(-1)

# create a list of OMERO.FigureIDs in .csv file
def list_figures():
    y = open(zegami_csv,'w')
    z = csv.writer(y)
    z.writerow(["figure_id","Gene","Collection", "Compartment","Probe"])

    for fig in conn.getObjects('FileAnnotation',
            attributes={'ns': 'omero.web.figure.json'}):
        filename = fig.getFileName()
        #if 'zegami1' not in filename and 'zegami2' not in filename:
        if 'zegami3' not in filename:
            continue
        fig_metadata = filename.split('_')
        figure_id = ('%d' % (fig.getId()))
        Gene = ('%s' % (fig_metadata[0]))
        Collection = ('%s' % (fig_metadata[1]))
        Compartment = ('%s' % (fig_metadata[2]))
        Probe = ('%s' % (fig_metadata[3]))
        min_info = figure_id,Gene,Collection,Compartment,Probe
	print ('extracting:', min_info)
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
            try:
                # get .json text from the Figure and write .json file
                fig_json = json.loads("".join(fig.getFileInChunks()))
                with open(os.path.join(outdir, str(fig_ID)+'.json'), 'w') as fh:
                    json.dump(fig_json, fh)
                    print ('downloaded figure:', fig_ID)
            except:
                print (fig_ID, 'does not exist')
        except:
            pass

        # open .json file
        json_path = os.path.join(outdir, str(fig_ID)+'.json')
        with open(json_path, 'r') as fh:
            fig_text = fh.read()

        # build jpg file
        fig_json = json.loads(fig_text)
        if int(fig_json['page_count']) > 1:
            raise RuntimeError("more than one page for figure id '%d'" % fig_id)

        export_params = {
            'Figure_JSON' : fig_text,
            'Webclient_URI': 'https://omero1.bioch.ox.ac.uk',
            'Export_Option' : 'TIFF', # change to jpeg
        }
        fig_export = TiffExport(conn, export_params,
                                export_images=False)
        def get_figure_file_name(page=None):
            return os.path.join(outdir, str(fig_ID)+'.jpg')
        fig_export.get_figure_file_name = get_figure_file_name

        try:
            fig_export.build_figure()
            print ('built:', str(fig_ID)+'.jpg')

        except:
            print("failed to build figure",str(fig_ID)+'.jpg')

def convert_jpg_to_png():
    jpg_files = os.listdir(outdir)
    for jpg in jpg_files:
        if jpg.endswith('.jpg'):
            im = Image.open(os.path.join(outdir, jpg))
            im.save(os.path.join(outdir, jpg.replace('.jpg','.png')))
            print ('converted ', jpg, 'to .png')

list_figures()
figure_json_to_jpg()
convert_jpg_to_png()

# Convert .jpg to .png
#print ("Converting .jpgs to .pngs ...")
#os.system('mogrify -density 400 -background white -alpha remove -format png ./*.jpg[0]')

conn.close
