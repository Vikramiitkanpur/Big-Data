#!/usr/bin/env python
# coding: utf-8

# In[7]:


import vtk

def extract_isocontour(data, isovalue):
    # Initialize VTK points and cell array
    contour_points = vtk.vtkPoints()
    contour_cells = vtk.vtkCellArray()

    for cellId in range(data.GetNumberOfCells()):
        cell = data.GetCell(cellId)
        isocontour_points_list = []# List to store interpolated points
        pointcount=0
       
        # Get the indices of the cell vertices
        pid1 = cell.GetPointId(0)
        pid2 = cell.GetPointId(1)
        pid3 = cell.GetPointId(3)
        pid4 = cell.GetPointId(2)
        
        # Get pressure values at each vertex
        dataArr = data.GetPointData().GetArray('Pressure')
        val1 = dataArr.GetTuple1(pid1)
        val2 = dataArr.GetTuple1(pid2)
        val3 = dataArr.GetTuple1(pid3)
        val4 = dataArr.GetTuple1(pid4)
        
        # Check for isovalue crossings and interpolate if needed
        # Append interpolated points to isocontour_points_list
        # Increment pointcount as needed
        if ((val1 > isovalue and val2 <= isovalue) or (val1 <= isovalue and val2 > isovalue)) and (pointcount <2):
            interp_factor = (isovalue - val1) / (val2 - val1)
            isocontour_point = [0.0, 0.0]
            isocontour_point[0] = data.GetPoint(pid1)[0] + interp_factor * (data.GetPoint(pid2)[0] - data.GetPoint(pid1)[0])
            isocontour_point[1] = data.GetPoint(pid1)[1] + interp_factor * (data.GetPoint(pid2)[1] - data.GetPoint(pid1)[1])
            isocontour_points_list.append(isocontour_point)
            pointcount += 1

        if ((val2 > isovalue and val3 <= isovalue) or (val2 <= isovalue and val3 > isovalue ))and (pointcount < 2):
            interp_factor = (isovalue - val2) / (val3 - val2)
            isocontour_point = [0.0, 0.0]
            isocontour_point[0] = data.GetPoint(pid2)[0] + interp_factor * (data.GetPoint(pid3)[0] - data.GetPoint(pid2)[0])
            isocontour_point[1] = data.GetPoint(pid2)[1] + interp_factor * (data.GetPoint(pid3)[1] - data.GetPoint(pid2)[1])
            isocontour_points_list.append(isocontour_point)
            pointcount += 1

        if ((val3 > isovalue and val4 <= isovalue) or (val3 <= isovalue and val4 > isovalue)) and (pointcount < 2):
            interp_factor = (isovalue - val3) / (val4 - val3)
            isocontour_point = [0.0, 0.0]
            isocontour_point[0] = data.GetPoint(pid3)[0] + interp_factor * (data.GetPoint(pid4)[0] - data.GetPoint(pid3)[0])
            isocontour_point[1] = data.GetPoint(pid3)[1] + interp_factor * (data.GetPoint(pid4)[1] - data.GetPoint(pid3)[1])
            isocontour_points_list.append(isocontour_point)
            pointcount += 1

        if ((val4 > isovalue and val1 <= isovalue) or (val4 <= isovalue and val1 > isovalue ))and (pointcount < 2):
            interp_factor = (isovalue - val4) / (val1 - val4)
            isocontour_point = [0.0, 0.0]
            isocontour_point[0] = data.GetPoint(pid4)[0] + interp_factor * (data.GetPoint(pid1)[0] - data.GetPoint(pid4)[0])
            isocontour_point[1] = data.GetPoint(pid4)[1] + interp_factor * (data.GetPoint(pid1)[1] - data.GetPoint(pid4)[1])
            isocontour_points_list.append(isocontour_point)
            pointcount += 1
        
         # Create VTK points and cells for the extracted isocontour
        if len(isocontour_points_list) ==2:
            pointId1 = contour_points.InsertNextPoint(isocontour_points_list[0][0], isocontour_points_list[0][1], 0.0)
            pointId2 = contour_points.InsertNextPoint(isocontour_points_list[1][0], isocontour_points_list[1][1], 0.0)
            cellId = contour_cells.InsertNextCell(2)
            contour_cells.InsertCellPoint(pointId1)
            contour_cells.InsertCellPoint(pointId2)

    # Create a vtkPolyData containing the isocontour
    isocontour_polydata = vtk.vtkPolyData()
    isocontour_polydata.SetPoints(contour_points)
    isocontour_polydata.SetLines(contour_cells)

    return isocontour_polydata

def write_vtp_file(polydata, output_filename):
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(polydata)
    writer.SetFileName(output_filename)
    writer.Write()

def main():
    # Read input data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName('Isabel_2D.vti')
    reader.Update()
    data = reader.GetOutput()

    isovalue = float(input("Enter isovalue: "))  # Prompt user for isovalue input

    # Extract isocontour and write to VTP file
    isocontour_polydata = extract_isocontour(data, isovalue)
    output_filename = 'output_contour.vtp'
    write_vtp_file(isocontour_polydata, output_filename)
    
    # Visualization using VTK
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(isocontour_polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(1000, 1000) 
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()


# In[ ]:




