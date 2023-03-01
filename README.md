# check_infoot

This code is intended for use of S-PLUS members to check if their objects are located within S-PLUS and if they were already observed or not.

Requirments:
- python 3.5+
- astropy

Usage: check_infoot.py [--option] [entry]

         Calculates if the coordinates provided are within the S-PLUS footprint.

        --help, -h:             print this help

        --coordinates, -c       coordinates for the target.
                                ra,dec => hh:mm:ss,dd:mm:ss. They must be separated
                                by a comma. Format can be hour or deg, but must
                                be specified using --deg or --hour. Default is hour.

        --coords_file, -f       File containing a minimum of two columns containing
                                RA and DEC. These columns must be named cap size as
                                RA,DEC. Format can be hour or deg, but must
                                be specified using --deg or --hour. Default is hour.

        --cformat, -d           ['deg' | 'hour'] tells the format of the input RA coordinates.
                                Default is hour. Dec is always assumed as deg.``
                                
                           
# Visualizing data over the S-PLUS footprint

1. Install Aladin from [https://aladin.u-strasbg.fr/java/nph-aladin.pl?frame=downloading](https://aladin.u-strasbg.fr/java/nph-aladin.pl?frame=downloading)

2. Open Aladin in your computer and load the table **tiles_nc.csv** and the filter **Filter0.ajs** that are part of this repository

3. Go to Overlay -> Create a new drawing plane

4. Load your table containing at least two columns for Ra and Dec. Your sources will be shown as symbols (aka small squares, circles, etc.) over the larger squares corresponding to the S-PLUS footprint.
