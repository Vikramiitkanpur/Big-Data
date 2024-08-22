#!/usr/bin/env python
# coding: utf-8

# In[2]:


import vtk

# Step 1: Load 3D Data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Isabel_3D.vti")  
reader.Update()

# Step 2: Set up Color and Opacity Transfer Functions
colour_change = vtk.vtkColorTransferFunction()
colour_change.AddRGBPoint(-4931.54, 0, 1, 1)
colour_change.AddRGBPoint(-2508.95, 0, 0, 1)
colour_change.AddRGBPoint(-1873.9, 0, 0, 0.5)
colour_change.AddRGBPoint(-1027.16, 1, 0, 0)
colour_change.AddRGBPoint(-298.031, 1, 0.4, 0)
colour_change.AddRGBPoint(2594.97, 1, 1, 0)

opacity_change = vtk.vtkPiecewiseFunction()
opacity_change.AddPoint(-4931.54, 1)
opacity_change.AddPoint(101.815, 0.002)
opacity_change.AddPoint(2594.97, 0.0)

# Step 3: Volume Rendering Setup
volume_rendering = vtk.vtkSmartVolumeMapper()
volume_rendering.SetInputConnection(reader.GetOutputPort())

volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(colour_change) #set all colour 
volume_property.SetScalarOpacity(opacity_change) # set opacity 

phongShading = False  
if input("Do you want to use Phong shading? (yes/no): ").lower() == "yes":
    phongShading = True
    volume_property.SetAmbient(0.5)
    volume_property.SetDiffuse(0.5)
    volume_property.SetSpecular(0.5)
    volume_property.SetSpecularPower(5)

# Step 4: Create Render Window, Renderer, and Interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(1000, 1000)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Step 5: Add Volume Actor to Renderer
volume = vtk.vtkVolume()
volume.SetMapper(volume_rendering)
volume.SetProperty(volume_property)
renderer.AddVolume(volume)


if phongShading:
    volume_property.ShadeOn()
    
# Step 6: Create Outline Actor
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_render = vtk.vtkPolyDataMapper()
outline_render.SetInputConnection(outline.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_render)
outline_actor.GetProperty().SetColor(0.2, 0.2, 0.2)  # Set outline color 
outline_actor.GetProperty().SetLineWidth(0.5) 

renderer.AddActor(outline_actor)  # Add outline actor to the renderer


# Step 7: Set Background Color and Render
renderer.SetBackground(1, 1, 1)  # Set background color to white
renderWindow.Render()

# Start the interaction
renderWindowInteractor.Start()


# In[ ]:




