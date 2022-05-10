# Herpich F.R. -- 2019-12-13
# herpich@usp.br
# last time modified: 2021-05-31

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import ascii
import sys
import os
from optparse import OptionParser


def arg_parser():
    parser = OptionParser(usage="""\
    \n
    CheckInFoot - check if your coordinate is within S-PLUS footprint!

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

    --cformat, -d           tells the format of the input RA coordinates.
                            Default is hour. Dec is always assumed as deg.

    """)

    parser.add_option('-c', '--coordinates',
                      type='string', action='store',
                      help="""Comma separated RA,Dec of the object""")
    parser.add_option('-f', '--coords_file',
                      type='string', action='store',
                      help="""csv file containing the objects coordinates""")
    parser.add_option('-d', '--cformat',
                      type='string', action='store',
                      help="""['hour' | 'deg'] format of the RA coordinates value.
                      Default is hour. Dec is always assumed as deg.""")

    (opts, args) = parser.parse_args()
    return opts, args


def check_infoot(coords=None, coords_file=None, formra=u.hour):
    """ check if objects are within the S-PLUS footprint """

    print('reading splus table...')
    pathtotilesfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'tiles_nc.csv')
    t = ascii.read(pathtotilesfile)
    c1 = SkyCoord(ra=t['RA'], dec=t['DEC'], unit=(u.hour, u.deg), frame='icrs')

    if coords is not None:
        inc = SkyCoord(ra=coords.split(',')[0], dec=coords.split(',')[1], unit=(formra, u.deg), frame='icrs')

        sep = c1.separation(inc)
        mask = sep.value < 1.0
        if mask.sum() == 0:
            print('\n')
            print('Not in the footprint...')
            sys.exit(0)
        else:
            print('\n')
            print('In the footprint')
            print('----------------------')
            print('TILE STATUS SEPARATION')
            print('----------------------')
            for i in range(mask.sum()):
                print(t['NAME'][mask][i], t['STATUS'][mask][i], sep.value[mask][i])
            print('If STATUS = {1, 2, 4, 5, 6}, the tile where the coordinates are located was already observed')
    elif coords_file is not None:
        t2 = ascii.read(coords_file)
        c2 = SkyCoord(ra=t2['RA'], dec=t2['DEC'],
                      unit=(formra, u.deg), frame='icrs')
        idx, d2d, d3d = c2.match_to_catalog_sky(c1)
        max_sep = 1.0 * u.deg
        sep_constraint = d2d < max_sep
        status = t['STATUS'][idx]
        status[~sep_constraint] = -10
        tile = t['NAME'][idx]
        tile[~sep_constraint] = '-'
        t2['TILE'] = tile
        t2['STATUS'] = status
        outname = coords_file.split('.')[0] + '_matched.csv'
        print('saving file', outname)
        t2.write(outname, overwrite=True)
        print('Your results are within the table', outname)
        print('If STATUS = {1, 2, 4, 5, 6}, the tile where the coordinates are located was already observed')

    else:
        raise IOError('wrong input coordinates format. Check -h or --help for help')

    return

if __name__ == '__main__':
    __version__ = '0.3.1'
    moddate = '2022-05-10'

    initext = """
        ===================================================================
                        CheckInFoot - v%s - %s
                 This version is not yet completely debugged
                 In case of crashes, please send the log to:
                    Herpich F. R. fabiorafaelh@gmail.com
        ===================================================================
        """ % (__version__, moddate)
    print(initext)

    opts, args = arg_parser()
    coords = opts.coordinates
    coords_file = opts.coords_file
    forma = opts.cformat

    if (forma == 'deg'):
        formra = u.deg
    elif (forma == 'hour') or (forma is None):
        formra = u.hour
    else:
        raise IOError('wrong input coordinates format. Check -h or --help for help')

    check_infoot(coords=coords, coords_file=coords_file, formra=formra)
