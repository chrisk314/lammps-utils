# LAMMPS Utils

Utilities for converting data to and from LAMMPS dump formats.

### Installation

Just clone and pip install as below:

```bash
git clone git@github.com:chrisk314/lammps-utils.git
cd lammps-utils
pip install -e .
```

Installing in develop mode allows you to add your own custom dump loader functions. See the
docstrings! ;-)

### Loading data from a dump file

Data can be loaded from a specified LAMMPS dump file using the `load_from_dump_file` function .

```python
from lammps_utils import load

fname = './dump.connectivity'

data = load.load_from_dump_file(fname)
```

The above code will extract all data from the dump file into a list containing data for
 each time step in order. The data has the following format:

 ```
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
 ```

 By default the format of the atom data in the dump file will be inferred by checking the line
 specifying the atom fields in the file such as this one:

 ```
ITEM: ATOMS id x y z diameter v_density c_conn 
 ```

 A structured array will be produced allowing access to the data by field name. 
 
```python
atom_data = data[0][3]  # Get atom data from first time step

x = atom_data['x']
diam = atom_data['diameter']
```

 Often it is preferable to work with an `ndarray` object instead. There is a utility function to perform the
 conversion.


```python
atom_data = load.as_ndarray(atom_data)  # Convert atom data to ndarray format
```

