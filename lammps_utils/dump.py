import h5py as h5
import vtk


def create_vtk_polydata(pos, attrs=[]):
    point_ids = vtk.vtkIdList()
    point_ids.SetNumberOfIds(len(pos))
    
    for i in range(len(pos)):
        point_ids.InsertNextId(i)

    points = vtk.vtkPoints()
    for x in pos:
        points.InsertNextPoint(*x)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    for attr in attrs:
        attr_name, attr_type, attr_comp, attr_data = attr
        if attr_type == 'int':
            vtk_attr = vtk.vtkIntArray()
        elif attr_type == 'float':
            vtk_attr = vtk.vtkDoubleArray()
        else:
            raise Exception('attribute data type %s not supported' % attr_type)
        vtk_attr.SetNumberOfComponents(attr_comp)
        vtk_attr.SetName(attr_name)
        for x in attr_data:
            vtk_attr.InsertNextValue(x)
        polydata.GetPointData().AddArray(vtk_attr)

    return polydata


def write_vtk_polydata(fname, pos, attrs=[]):
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(create_vtk_polydata(pos, attrs=attrs))
    writer.SetFileName(fname)
    writer.SetDataModeToAscii()
    writer.Update()


def write_h5_mf(fname, p_data):
    fields = list(p_data.dtype.names)
    
    f = h5.File(fname, 'w')

    f['Number'] = p_data['id']
    f['Xpos'], f['Ypos'], f['Zpos'] = p_data['x'], p_data['y'], p_data['z']
    f['Diameter'] = p_data['diameter']
    if 'vx' in fields:
        f['Vx'], f['Vy'], f['Vz'] = p_data['vx'], p_data['vy'], p_data['vz']

