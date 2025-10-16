"""
PROFESSIONAL PARAMETRIC BASE CABINET
Based on industry-standard cabinet construction
All measurements in inches
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import System

def create_parametric_cabinet(width=30, depth=24, height=30.5, shelf_count=1, thickness=0.75):
    """
    Professional base cabinet with proper construction details
    
    Parameters:
    - width: Cabinet width (inches)
    - depth: Cabinet depth (inches)
    - height: Cabinet height (inches)
    - shelf_count: Number of adjustable shelves
    - thickness: Panel thickness (inches) - typically 0.75"
    """
    
    print(f"\n=== CREATING BASE CABINET ===")
    print(f"Size: {width}W x {depth}D x {height}H")
    print(f"Thickness: {thickness}\"")
    
    objects = []
    
    # ========== CABINET PARAMETERS (FROM XML) ==========
    back_thickness = 0.5
    side_width = depth - 0.875  # Sides are inset from back
    door_gap = 0.125  # Gap between doors
    top_gap = 0.125
    bottom_gap = 0
    
    # ========== LEFT SIDE PANEL ==========
    # Length=Height, Width=SideWidth, Thickness=0.75
    left_side = rg.Box(
        rg.Plane(rg.Point3d(0, 0, 0), rg.Vector3d.XAxis, rg.Vector3d.YAxis),
        rg.Interval(0, thickness),
        rg.Interval(0, side_width),
        rg.Interval(0, height)
    )
    left_id = sc.doc.Objects.AddBrep(left_side.ToBrep())
    objects.append(left_id)
    sc.doc.Objects.Find(left_id).Attributes.Name = "Side Left"
    print(f"  ✓ Left Side: {thickness}\" x {side_width}\" x {height}\"")
    
    # ========== RIGHT SIDE PANEL ==========
    right_side = rg.Box(
        rg.Plane(rg.Point3d(width - thickness, 0, 0), rg.Vector3d.XAxis, rg.Vector3d.YAxis),
        rg.Interval(0, thickness),
        rg.Interval(0, side_width),
        rg.Interval(0, height)
    )
    right_id = sc.doc.Objects.AddBrep(right_side.ToBrep())
    objects.append(right_id)
    sc.doc.Objects.Find(right_id).Attributes.Name = "Side Right"
    print(f"  ✓ Right Side: {thickness}\" x {side_width}\" x {height}\"")
    
    # ========== BACK PANEL ==========
    # Goes in groove, width = Width-1 (fits between sides with grooves)
    back_width = width - 1.0
    back = rg.Box(
        rg.Plane(rg.Point3d(0.5, side_width - 1 + back_thickness, 0), 
                 rg.Vector3d.XAxis, rg.Vector3d.ZAxis),
        rg.Interval(0, back_width),
        rg.Interval(0, back_thickness),
        rg.Interval(0, height)
    )
    back_id = sc.doc.Objects.AddBrep(back.ToBrep())
    objects.append(back_id)
    sc.doc.Objects.Find(back_id).Attributes.Name = "Back"
    print(f"  ✓ Back: {back_width}\" x {back_thickness}\" x {height}\"")
    
    # ========== BOTTOM PANEL ==========
    bottom_width = width - 1.5  # Fits between sides
    bottom_depth = side_width - 1 - 0.0625
    bottom = rg.Box(
        rg.Plane(rg.Point3d(thickness, 0.0625, 0), rg.Vector3d.XAxis, rg.Vector3d.YAxis),
        rg.Interval(0, bottom_width),
        rg.Interval(0, bottom_depth),
        rg.Interval(0, thickness)
    )
    bottom_id = sc.doc.Objects.AddBrep(bottom.ToBrep())
    objects.append(bottom_id)
    sc.doc.Objects.Find(bottom_id).Attributes.Name = "Bottom"
    print(f"  ✓ Bottom: {bottom_width}\" x {bottom_depth}\" x {thickness}\"")
    
    # ========== FRONT STRETCHER (TOP RAIL) ==========
    stretcher_width = 4.0
    front_stretcher = rg.Box(
        rg.Plane(rg.Point3d(thickness, 4.0625, height - stretcher_width), 
                 rg.Vector3d.XAxis, rg.Vector3d.YAxis),
        rg.Interval(0, bottom_width),
        rg.Interval(0, thickness),
        rg.Interval(0, stretcher_width)
    )
    stretcher_id = sc.doc.Objects.AddBrep(front_stretcher.ToBrep())
    objects.append(stretcher_id)
    sc.doc.Objects.Find(stretcher_id).Attributes.Name = "Front Stretcher"
    print(f"  ✓ Front Stretcher: {bottom_width}\" x {stretcher_width}\" x {thickness}\"")
    
    # ========== BACK STRETCHER ==========
    back_stretcher = rg.Box(
        rg.Plane(rg.Point3d(thickness, side_width - 1, height - stretcher_width), 
                 rg.Vector3d.XAxis, rg.Vector3d.YAxis),
        rg.Interval(0, bottom_width),
        rg.Interval(0, thickness),
        rg.Interval(0, stretcher_width)
    )
    back_stretch_id = sc.doc.Objects.AddBrep(back_stretcher.ToBrep())
    objects.append(back_stretch_id)
    sc.doc.Objects.Find(back_stretch_id).Attributes.Name = "Back Stretcher"
    print(f"  ✓ Back Stretcher: {bottom_width}\" x {stretcher_width}\" x {thickness}\"")
    
    # ========== ADJUSTABLE SHELVES ==========
    if shelf_count > 0:
        shelf_width = bottom_width - 0.0625
        shelf_depth = side_width - 1.25
        
        # Calculate even spacing (FROM XML FORMULA)
        available_height = height - 1.5 - (shelf_count * thickness)
        shelf_spacing = available_height / (shelf_count + 1)
        
        for i in range(shelf_count):
            z_pos = thickness + ((i + 1) * shelf_spacing) + (i * thickness)
            
            shelf = rg.Box(
                rg.Plane(rg.Point3d(thickness + 0.03125, 0.25, z_pos), 
                         rg.Vector3d.XAxis, rg.Vector3d.YAxis),
                rg.Interval(0, shelf_width),
                rg.Interval(0, shelf_depth),
                rg.Interval(0, thickness)
            )
            shelf_id = sc.doc.Objects.AddBrep(shelf.ToBrep())
            objects.append(shelf_id)
            sc.doc.Objects.Find(shelf_id).Attributes.Name = f"Shelf {i+1}"
        
        print(f"  ✓ Shelves ({shelf_count}): {shelf_width}\" x {shelf_depth}\" x {thickness}\"")
    
    # ========== DOORS (TWO DOOR CONFIGURATION) ==========
    door_height = height - top_gap - bottom_gap
    door_width = (width - door_gap) / 2.0 - door_gap
    
    # LEFT DOOR
    left_door = rg.Box(
        rg.Plane(rg.Point3d(door_gap/2, -0.875, bottom_gap), 
                 rg.Vector3d.XAxis, rg.Vector3d.YAxis),
        rg.Interval(0, door_width),
        rg.Interval(0, thickness),
        rg.Interval(0, door_height)
    )
    left_door_id = sc.doc.Objects.AddBrep(left_door.ToBrep())
    objects.append(left_door_id)
    sc.doc.Objects.Find(left_door_id).Attributes.Name = "Door Left"
    
    # RIGHT DOOR
    right_door = rg.Box(
        rg.Plane(rg.Point3d(width/2 + door_gap/2, -0.875, bottom_gap), 
                 rg.Vector3d.XAxis, rg.Vector3d.YAxis),
        rg.Interval(0, door_width),
        rg.Interval(0, thickness),
        rg.Interval(0, door_height)
    )
    right_door_id = sc.doc.Objects.AddBrep(right_door.ToBrep())
    objects.append(right_door_id)
    sc.doc.Objects.Find(right_door_id).Attributes.Name = "Door Right"
    print(f"  ✓ Doors (2): {door_width:.3f}\" x {thickness}\" x {door_height}\"")
    
    # ========== ADD REFERENCE POINTS FOR HARDWARE ==========
    # Hinge locations (2 hinges per door, from XML)
    hinge_z_positions = [3.0, height - 3.0]
    
    # Left door hinges
    for i, z in enumerate(hinge_z_positions):
        pt = sc.doc.Objects.AddPoint(rg.Point3d(thickness, 1.46, z))
        sc.doc.Objects.Find(pt).Attributes.Name = f"Hinge Left {i+1}"
        objects.append(pt)
    
    # Right door hinges
    for i, z in enumerate(hinge_z_positions):
        pt = sc.doc.Objects.AddPoint(rg.Point3d(width - thickness, 1.46, z))
        sc.doc.Objects.Find(pt).Attributes.Name = f"Hinge Right {i+1}"
        objects.append(pt)
    
    # Door pull locations (FROM XML FORMULA)
    pull_from_edge = 4.625  # 4.625" from edge
    pull_from_top = 0.0625
    
    # Left door pull
    left_pull_x = width/2 - pull_from_edge - door_gap/2
    pull_pt_left = sc.doc.Objects.AddPoint(rg.Point3d(left_pull_x, -0.875, height - pull_from_top - top_gap))
    sc.doc.Objects.Find(pull_pt_left).Attributes.Name = "Pull Left"
    objects.append(pull_pt_left)
    
    # Right door pull
    right_pull_x = width/2 + pull_from_edge + door_gap/2
    pull_pt_right = sc.doc.Objects.AddPoint(rg.Point3d(right_pull_x, -0.875, height - pull_from_top - top_gap))
    sc.doc.Objects.Find(pull_pt_right).Attributes.Name = "Pull Right"
    objects.append(pull_pt_right)
    
    print(f"  ✓ Hardware reference points added")
    
    # ========== ORGANIZE IN LAYER ==========
    layer_name = f"Cabinet_{width:.0f}x{depth:.0f}x{height:.1f}"
    layer_index = sc.doc.Layers.FindName(layer_name)
    
    if layer_index < 0:
        layer_index = sc.doc.Layers.Add(layer_name, System.Drawing.Color.FromArgb(139, 90, 43))
    
    for obj_id in objects:
        obj = sc.doc.Objects.Find(obj_id)
        if obj:
            obj.Attributes.LayerIndex = layer_index
            obj.CommitChanges()
    
    sc.doc.Views.Redraw()
    
    print(f"\n=== SUCCESS ===")
    print(f"Created {len(objects)} components")
    print(f"Layer: {layer_name}")
    print(f"\nCUT LIST:")
    print(f"  • Sides (2): {thickness}\" x {side_width}\" x {height}\"")
    print(f"  • Bottom (1): {bottom_width}\" x {bottom_depth}\" x {thickness}\"")
    print(f"  • Back (1): {back_width}\" x {back_thickness}\" x {height}\"")
    print(f"  • Stretchers (2): {bottom_width}\" x {stretcher_width}\" x {thickness}\"")
    print(f"  • Doors (2): {door_width:.3f}\" x {thickness}\" x {door_height}\"")
    if shelf_count > 0:
        print(f"  • Shelves ({shelf_count}): {shelf_width}\" x {shelf_depth}\" x {thickness}\"")
    
    return objects
