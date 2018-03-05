import sys

import numpy as np

CONVERT_TYPE_MAP = {'int': int, 'float': float}
FIELD_TYPE_MAP = {'id': 'int', 'connectivity': 'int'}


class DumpLoaderError(Exception):
    pass


def as_ndarray(array):
    """Return ndarray representation of a structured array."""
    return array.view((np.float64, len(array.dtype.names)))


def proc_str(s):
    """Return string stripped of whitespace and lowercase"""
    return s.strip().lower()


def get_atom_data_spec(s):
    """Convert string containing data field names into tuple of data types."""
    fields = proc_str(s).split()[2:]
    return [(field, FIELD_TYPE_MAP.get(field, 'float')) for field in fields]


def dump_loader_conn_diam(f, p_num, **kwargs):
    """
    Return numpy array of particle data for p_num particles from file handle f.
    Expected data format:
        id:int x:float y:float z:float diameter:float connectivty:int
    :param f file: file object from which to read data
    :param p_num: number of particles for which to extract data
    :return numpy.ndarray: array of particle data sorted by particle id
    """
    p_data = np.empty((p_num,6))
    for i in xrange(p_num):
        p_data[i] = np.array([float(tok) for tok in proc_str(f.readline()).split()])
    return p_data[p_data[:,0].argsort()][:,(1,2,3,4,5)]


def dump_loader_generic(f, p_num, spec=None):
    """Load data from LAMMPS dump file using the provided data type specification."""
    if not spec:
        raise DumpLoaderError('No data spec provided to %s' % sys._getframe().f_code.co_name)
    return np.genfromtxt(f, dtype=spec, max_rows=p_num)


def load_from_dump_file(fname, load_func=dump_loader_generic, ts_start=None, ts_stop=None):
    """
    Return list containing dump data for each timestep of simulation in the format:
    [
        (
            3000000,                                                   # timestep
            383,                                                       # number of particles
            array([ 0.       ,  0.0067592,  0.       ,  0.0067592,     # domain dimensions
                    0.       , 0.0067592]),
            array([                                                    # particle data
                [  0.00000000e+00,   5.59600000e-04,   8.75341000e-04,
                    4.43585000e-05,   1.00528000e-03],
                [  0.00000000e+00,   2.56164000e-04,   3.86693000e-04,
                    5.50167000e-04,   5.09240000e-04],
                ...
            ])
        ),
        ...
    ]
    Note: the format of the particle data returned depends on the choice of load_func
    :param fname str: path of dump file
    :param load_func: function for loading particle data which returns numpy array
    :param ts_start int: timestep at which to start data extraction (inclusive)
    :param ts_start int: timestep at which to stop data extraction (inclusive)
    :return list: list of tuples containing simulation data as described above
    """
    data_stack = []
    with open(fname, 'r') as f:
        while True:
            try:
                l = next(f)
            except StopIteration:
                break
            l = proc_str(l)
            if 'item: timestep' in l:
                timestep = int(proc_str(next(f)))
                if ts_stop and timestep > ts_stop:
                    break
            if 'item: number of atoms' in l:
                p_num = int(proc_str(next(f)))
            if 'item: box bounds' in l:
                xlo, xhi = [float(tok) for tok in proc_str(next(f)).split()]
                ylo, yhi = [float(tok) for tok in proc_str(next(f)).split()]
                zlo, zhi = [float(tok) for tok in proc_str(next(f)).split()]
                bounds = np.array([xlo, xhi, ylo, yhi, zlo, zhi])
            if 'item: atoms' in l:
                if ts_start and timestep < ts_start:
                    continue
                try:
                    p_data = load_func(f, p_num, spec=get_atom_data_spec(l))
                except:
                    raise DumpLoaderError('Could not load data for timestep %d' % timestep)
                data_stack.append((timestep, p_num, bounds, p_data))
    return data_stack
