"""
Thierry Bertin-Mahieux (2010) Columbia University
tb2332@columbia.edu

Code to quickly see the content of an HDF5 file.

This is part of the Million Song Dataset project from
LabROSA (Columbia University) and The Echo Nest.


Copyright 2010, Thierry Bertin-Mahieux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import hdf5_getters
import hdf5_utils
import numpy as np


def die_with_usage():
    """ HELP MENU """
    print 'display_song.py'
    print 'T. Bertin-Mahieux (2010) tb2332@columbia.edu'
    print 'to quickly display all we know about a song'
    print 'usage:'
    print '   python display_song.py <HDF5 file> <OPT: song idx> <OPT: specific getter>'
    print 'example:'
    print '   python display_song.py mysong.h5 0 danceability'
    sys.exit(0)


if __name__ == '__main__':
    """ MAIN """

    # help menu
    if len(sys.argv) < 2:
        die_with_usage()

    # get params
    hdf5path = sys.argv[1]
    songidx = 0
    if len(sys.argv) > 2:
        songidx = int(sys.argv[2])
    onegetter = ''
    if len(sys.argv) > 3:
        onegetter = sys.argv[3]

    # sanity check
    if not os.path.isfile(hdf5path):
        print 'ERROR: file',hdf5path,'does not exist.'
        sys.exit(0)
    h5 = hdf5_utils.open_h5_file_read(hdf5path)
    numSongs = hdf5_getters.get_num_songs(h5)
    if songidx >= numSongs:
        print 'ERROR: file contains only',numSongs
        sys.exit(0)

    # get all getters
    getters = filter(lambda x: x[:4] == 'get_', hdf5_getters.__dict__.keys())
    getters.remove("get_num_songs") # special case
    if onegetter == 'num_songs' or onegetter == 'get_num_songs':
        getters = []
    elif onegetter != '':
        if onegetter[:4] != 'get_':
            onegetter = 'get_' + onegetter
        try:
            getters.index(onegetter)
        except ValueError:
            print 'ERROR: getter requested:',onegetter,'does not exist.'
            sys.exit(0)
        getters = [onegetter]
    getters = np.sort(getters)

    # print them
    for getter in getters:
        res = hdf5_getters.__getattribute__(getter)(h5,songidx)
        if res.__class__.__name__ == 'ndarray':
            print getter[4:]+": shape =",res.shape
        else:
            print getter[4:]+":",res


    # done
    print 'DONE, showed song',songidx,'/',numSongs-1,'in file:',hdf5path



    
