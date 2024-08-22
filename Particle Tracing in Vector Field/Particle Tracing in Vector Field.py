import vtk 
import numpy as np
from vtk import *

# Read the vector field data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("tornado3d_vector.vti")
reader.Update()
data = reader.GetOutput()

# Define seed location, step size, and maximum number of steps
seed_location = np.array([0, 0, 7.0])
step_size = 0.05
max_steps = 1000

# Function to interpolate velocity at a given point in the vector field
def interpolate_velocity(point, vector_field):
    # Create a single point for probe filter
    input_points = vtk.vtkPoints()
    input_points.InsertNextPoint(point)

    # Create vtkPolyData object to hold the single point
    input_data = vtk.vtkPolyData()
    input_data.SetPoints(input_points)

    # Create vtkProbeFilter object
    probe_filter = vtk.vtkProbeFilter()

    # Set input and source data for the probe filter
    probe_filter.SetInputData(input_data)
    probe_filter.SetSourceData(vector_field)

    # Set the point where interpolation is to be performed
    probe_filter.Update()

    # Return the interpolated velocity
    return probe_filter.GetOutput().GetPointData().GetVectors().GetTuple(0)

# Function to perform RK4 integration forward in the vector field
def rk4_integrate_forward(data, start_point_f, step_size, max_steps):
    # Initialize an empty list to store the points along the streamline
    streamline_f = []
    
    # Get the bounds of the vector field dataset
    field_bounds = data.GetBounds()

    # Perform RK4 integration forward
    for _ in range(max_steps):
        
        # Compute RK4 coefficients
        k1 = interpolate_velocity(start_point_f, data)
        k2 = interpolate_velocity([start_point_f[i] + k1[i] * (step_size / 2) for i in range(3)], data)
        k3 = interpolate_velocity([start_point_f[i] + k2[i] * (step_size / 2) for i in range(3)], data)
        k4 = interpolate_velocity([start_point_f[i] + k3[i] * step_size for i in range(3)], data)
        
        # Compute the next point using RK4 formula
        next_point = [start_point_f[i] + (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * (step_size / 6) for i in range(3)]
        
        # Check if the next point is within the bounds of the vector field dataset
        if (field_bounds[0] <= next_point[0] <= field_bounds[1]) and \
           (field_bounds[2] <= next_point[1] <= field_bounds[3]) and \
           (field_bounds[4] <= next_point[2] <= field_bounds[5]):
            # Append the next point to the streamline and update the start point
            streamline_f.append(next_point)
            start_point_f = next_point
        else:
            # Break the loop if the next point is outside the bounds
            break
    
    return streamline_f

# Function to perform RK4 integration backward in the vector field
def rk4_integrate_backward(data, start_point_b, step_size, max_steps):
    # Initialize an empty list to store the points along the streamline
    streamline_b = []
    
    # Get the bounds of the vector field dataset
    field_bounds = data.GetBounds()

    # Perform RK4 integration backward
    for _ in range(max_steps):
        
        
        # Compute RK4 coefficients
        k_1 = interpolate_velocity(start_point_b, data)
        k_2 = interpolate_velocity([start_point_b[i] + k_1[i] * (-step_size / 2) for i in range(3)], data)
        k_3 = interpolate_velocity([start_point_b[i] + k_2[i] * (-step_size / 2) for i in range(3)], data)
        k_4 = interpolate_velocity([start_point_b[i] + k_3[i] * (-step_size) for i in range(3)], data)
        
        # Compute the next point using RK4 formula
        next_point = [start_point_b[i] + (k_1[i] + 2 * k_2[i] + 2 * k_3[i] + k_4[i]) * (-step_size / 6) for i in range(3)]
        
        # Check if the next point is within the bounds of the vector field dataset
        if (field_bounds[0] <= next_point[0] <= field_bounds[1]) and \
           (field_bounds[2] <= next_point[1] <= field_bounds[3]) and \
           (field_bounds[4] <= next_point[2] <= field_bounds[5]):
            # Append the next point to the streamline and update the start point
            streamline_b.append(next_point)
            start_point_b = next_point
        else:
            # Break the loop if the next point is outside the bounds
            break
    
    return streamline_b

# Function to combine forward and backward streamlines
def combine_streamlines(streamline_backward, streamline_forward):
    return streamline_backward + [seed_location.tolist()] + streamline_forward

# Function to create a VTKPolyData file from the streamline points
def create_streamline_vtp(streamline_points, filename):
    # Create vtkPoints to store the streamline points
    vtk_points = vtk.vtkPoints()
    for point in streamline_points:
        vtk_points.InsertNextPoint(point)

    # Create vtkCellArray to store the lines
    vtk_cells = vtk.vtkCellArray()
    for k in range(1, vtk_points.GetNumberOfPoints()):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, k - 1)
        line.GetPointIds().SetId(1, k)
        vtk_cells.InsertNextCell(line)

    # Create vtkPolyData to represent the streamline
    streamline_polydata = vtk.vtkPolyData()
    streamline_polydata.SetPoints(vtk_points)
    streamline_polydata.SetLines(vtk_cells)

    # Write the streamline to a VTKPolyData file (.vtp)
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(streamline_polydata)
    writer.Write()

# Perform RK4 integration forward
streamline_forward = rk4_integrate_forward(data, seed_location, step_size, max_steps)

# Perform RK4 integration backward
streamline_backward = rk4_integrate_backward(data, seed_location, step_size, max_steps)
streamline_backward.reverse()

# Combine forward and backward streamlines
combined_streamline = combine_streamlines(streamline_backward, streamline_forward)

# Create VTKPolyData file from the combined streamline points
create_streamline_vtp(combined_streamline, "mystream.vtp" )

# Read the VTKPolyData file
reader = vtkXMLPolyDataReader()
reader.SetFileName('mystream.vtp') 
reader.Update()
pdata = reader.GetOutput()

# Setup mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputData(pdata)
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(5) 
actor.GetProperty().SetColor(0,1,0)

# Setup render window, renderer, and interactor
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderWindow = vtkRenderWindow()
renderWindow.SetSize(800,800)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)

# Render the object
renderWindow.Render()
renderWindowInteractor.Start()
