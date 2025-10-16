"""
PARAMETRIC CABINET GENERATOR
Simple Python script for Rhino - No Grasshopper needed!
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc

def create_parametric_cabinet(width=3, depth=2, height=6, shelf_count=3, thickness=0.05):
    """
    Creates a parametric cabinet with shelves
    
    Parameters:
    - width: Cabinet width (feet/meters)
    - depth: Cabinet depth (feet/meters)
    - height: Cabinet height (feet/meters)
    - shelf_count: Number of internal shelves
    - thickness: Material thickness (feet/meters)
    """
    
    print(f"Creating cabinet: {width}x{depth}x{height} with {shelf_count} shelves")
    
    objects = []
    
    # BACK PANEL
    back_pts = [
        rg.Point3d(0, 0, 0),
        rg.Point3d(width, 0, 0),
        rg.Point3d(width, 0, height),
        rg.Point3d(0, 0, height),
        rg.Point3d(0, 0, 0)
    ]
    back = rg.Brep.CreateFromCornerPoints(back_pts[0], back_pts[1], back_pts[2], back_pts[3], sc.doc.ModelAbsoluteTolerance)
    if back:
        objects.append(sc.doc.Objects.AddBrep(back))
    
    # LEFT SIDE
    left_pts = [
        rg.Point3d(0, 0, 0),
        rg.Point3d(0, depth, 0),
        rg.Point3d(0, depth, height),
        rg.Point3d(0, 0, height),
        rg.Point3d(0, 0, 0)
    ]
    left = rg.Brep.CreateFromCornerPoints(left_pts[0], left_pts[1], left_pts[2], left_pts[3], sc.doc.ModelAbsoluteTolerance)
    if left:
        objects.append(sc.doc.Objects.AddBrep(left))
    
    # RIGHT SIDE
    right_pts = [
        rg.Point3d(width, 0, 0),
        rg.Point3d(width, depth, 0),
        rg.Point3d(width, depth, height),
        rg.Point3d(width, 0, height),
        rg.Point3d(width, 0, 0)
    ]
    right = rg.Brep.CreateFromCornerPoints(right_pts[0], right_pts[1], right_pts[2], right_pts[3], sc.doc.ModelAbsoluteTolerance)
    if right:
        objects.append(sc.doc.Objects.AddBrep(right))
    
    # BOTTOM
    bottom_pts = [
        rg.Point3d(0, 0, 0),
        rg.Point3d(width, 0, 0),
        rg.Point3d(width, depth, 0),
        rg.Point3d(0, depth, 0),
        rg.Point3d(0, 0, 0)
    ]
    bottom = rg.Brep.CreateFromCornerPoints(bottom_pts[0], bottom_pts[1], bottom_pts[2], bottom_pts[3], sc.doc.ModelAbsoluteTolerance)
    if bottom:
        objects.append(sc.doc.Objects.AddBrep(bottom))
    
    # TOP
    top_pts = [
        rg.Point3d(0, 0, height),
        rg.Point3d(width, 0, height),
        rg.Point3d(width, depth, height),
        rg.Point3d(0, depth, height),
        rg.Point3d(0, 0, height)
    ]
    top = rg.Brep.CreateFromCornerPoints(top_pts[0], top_pts[1], top_pts[2], top_pts[3], sc.doc.ModelAbsoluteTolerance)
    if top:
        objects.append(sc.doc.Objects.AddBrep(top))
    
    # SHELVES (evenly spaced)
    if shelf_count > 0:
        shelf_spacing = height / (shelf_count + 1)
        
        for i in range(1, shelf_count + 1):
            z_pos = i * shelf_spacing
            
            shelf_pts = [
                rg.Point3d(0, 0, z_pos),
                rg.Point3d(width, 0, z_pos),
                rg.Point3d(width, depth, z_pos),
                rg.Point3d(0, depth, z_pos),
                rg.Point3d(0, 0, z_pos)
            ]
            
            shelf = rg.Brep.CreateFromCornerPoints(shelf_pts[0], shelf_pts[1], shelf_pts[2], shelf_pts[3], sc.doc.ModelAbsoluteTolerance)
            if shelf:
                objects.append(sc.doc.Objects.AddBrep(shelf))
    
    sc.doc.Views.Redraw()
    
    print(f"Created {len(objects)} objects!")
    return objects
