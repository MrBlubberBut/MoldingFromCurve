bl_info = {
    "name": "Molding from Curve",
    "author": "Lukas Kawalec",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Create tab",
    "description": "Makes a molding from a curve and a mesh",
    "warning": "",
    "doc_url": "",
}

import bpy
import mathutils
from mathutils import Vector
from mathutils import Matrix
import builtins as __builtin__
import math

def loopOpen(angle):
    
    # Combines most of the functions into one loop
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    curveIndex = 0
    f = other
    origin = VertIndex
    face = (verticeCount + 2) - (verticeCount * 2)
    
    for v in cur.data.vertices[:-1]:
        
        curveIndex += 1
        origin += verticeCount
        f += verticeCount
        face += verticeCount
        
        if curveIndex == 1:
            extrude(0)
            
            if closed:
                move(1, 0, origin)
            else:
                move(1, curveIndex, origin)
        
        elif curveIndex == 2:
            shear(Vector((curveIndex, curveIndex - 1)), 1, Vector((f - verticeCount, origin - verticeCount)), angle)
            extrude(1)
            move(face, curveIndex, origin)
            fix(Vector((curveIndex, curveIndex - 1)), Vector((f - verticeCount, origin - verticeCount)), face, origin)
     
        else:
            shear(Vector((curveIndex, curveIndex - 1)), face - verticeCount, Vector((f - verticeCount, origin - verticeCount)), angle)
            extrude(face - verticeCount)
            move(face, curveIndex, origin)
            fix(Vector((curveIndex, curveIndex - 1)), Vector((f - verticeCount, origin - verticeCount)), face, origin)

def loopClosed(angle):
        
    # Combines most of the functions into one loop
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    curveIndex = 0
    f = other
    origin = VertIndex
    face = (verticeCount + 2) - (verticeCount * 2)
    
    for v in cur.data.vertices[:-1]:
        
        curveIndex += 1
        origin += verticeCount
        f += verticeCount
        face += verticeCount
        
        if curveIndex == 1:
            
            extrude(0)
            move(1, 0, origin)
            shear(Vector((1, 0)), 1, Vector((f, origin)), angle)
            extrude(1)
            move(face + verticeCount, curveIndex, origin + verticeCount)
            fix(Vector((1, 0)), Vector((f, origin)), face + verticeCount, origin + verticeCount)
            
        
        elif curveIndex < verticeCountCur:
            
            shear(Vector((curveIndex, curveIndex - 1)), face, Vector((f, origin)), angle)
            extrude(face)
            move(face + verticeCount, curveIndex, origin + verticeCount)
            fix(Vector((curveIndex, curveIndex - 1)), Vector((f, origin)), face + verticeCount, origin + verticeCount)
            
            if curveIndex == (verticeCountCur - 1):
                shear(Vector((0, verticeCountCur - 1)), face + verticeCount, Vector((f + verticeCount, origin + verticeCount)), angle)
                extrude(face + verticeCount)
                move(face + (verticeCount * 2), mwMol @ mol.data.vertices[0].co, origin + verticeCount)
                merge(curveIndex)
        
                
def merge(curveIndex):
    
    deselect(mol)
    origin = (curveIndex * verticeCount) + (verticeCount * 2)
    
    for v in range(verticeCount):
        mol.data.vertices[origin].select = True
        mol.data.vertices[v].select = True

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.merge(type = 'CENTER')
        bpy.ops.object.mode_set(mode = 'OBJECT')
    
        deselect(mol)
 
def fix(vec, FD, face, origin):
    
    # Scales the face by 0 to align it with the resh of the mesh
    index = face
    deselect(mol)
     
    normalvec = (cur.data.vertices[int(vec.x)].co - cur.data.vertices[int(vec.y)].co).normalized().to_4d()
    normalvec.w = 0
    vec = (mwCur @ normalvec).to_3d()
    vec.normalize()

    normalFD = (mol.data.vertices[int(FD.x)].co - mol.data.vertices[int(FD.y)].co).normalized().to_4d()
    normalFD.w = 0
    FD = (mwMol @ normalFD).to_3d()
    FD.normalize()

    cross = FD.cross(vec)
    cross.normalize()
    
    perp = vec.cross(cross)
    perp.normalize()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    deselect(mol)
    mol.data.polygons.active = index
    mol.data.polygons[index].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.transform.resize(center_override = mwMol @ mol.data.vertices[origin].co, 
    value = (1, 0, 1), 
    orient_matrix=((cross, vec, perp)))
    
    bpy.ops.object.mode_set(mode = 'OBJECT')

def executeShear(fd, vec, cross, face, fb, angle, direction):
    
    # Exexutes the shear according to the direction determined earlier
    deselect(mol)
    select(face)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    pos_before = mol.data.vertices[int(fd.y)].co.copy()

    origin = mathutils.Matrix.Translation(mwMol @ mol.data.vertices[int(fd.y)].co)
       
    if direction == "right":
        
        x = angle / 2
        y = math.radians(90 - x)
        v = (math.cos(y)) / (math.sin(y))
        
        bpy.ops.transform.shear(value = -v, orient_matrix=(vec, cross, fb))
        
        bpy.context.object.update_from_editmode()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        pos_after = mol.data.vertices[int(fd.y)].co
        
    elif direction == "left":
         
        x = angle / 2
        y = math.radians(90 - x)
        v = (math.cos(y)) / (math.sin(y))
        
        bpy.ops.transform.shear(value = v, orient_matrix=(vec, cross, fb))

        bpy.context.object.update_from_editmode()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        pos_after = mol.data.vertices[int(fd.y)].co
        
    elif direction == "up":
        
        x = angle / 2
        y = math.radians(90 - x)
        v = (math.cos(y)) / (math.sin(y))
        bpy.ops.transform.shear(value = -v, orient_axis='Y', orient_matrix=(vec, cross, fb))
        
        bpy.context.object.update_from_editmode()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        pos_after = mol.data.vertices[int(fd.y)].co
        
    elif direction == "down":
           
        x = angle / 2
        y = math.radians(90 - x)
        v = (math.cos(y)) / (math.sin(y))
        
        bpy.ops.transform.shear(value = v, orient_axis='Y', orient_matrix=(vec, cross, fb))
        
        bpy.context.object.update_from_editmode()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        pos_after = mol.data.vertices[int(fd.y)].co
    
    m = mathutils.Matrix.Translation(pos_after - pos_before)
    
    m2 = origin @ m.inverted() @ origin.inverted()
    
    for index in mol.data.polygons[face].vertices:
        vert = mol.data.vertices[index]
        vert.co = m2 @ vert.co

def select(face):
    
    # Selects a specific face of the mesh
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = mol
    mol.select_set(True)
    mol.data.polygons.active = face
    mol.data.polygons[face].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')

def deselect(obj):
    
    # Deselects everything in the mesh
    for f in obj.data.polygons:
        f.select = False
    for e in obj.data.edges:
        e.select = False
    for v in obj.data.vertices:
        v.select = False

def move(face, curveIndex, origin):
    
    # Moves the face to specified destination
    if isinstance(curveIndex, int):
        mol.data.polygons.active = face
        mol.data.polygons[face].select = True
        destination = (mwCur @ cur.data.vertices[curveIndex].co.copy()) - (mwMol @ mol.data.vertices[origin].co.copy())
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.transform.translate(value=destination, orient_type = 'GLOBAL')
        bpy.ops.object.mode_set(mode='OBJECT')
        
    else:
        mol.data.polygons.active = face
        mol.data.polygons[face].select = True
        destination = curveIndex - (mwMol @ mol.data.vertices[origin].co.copy())
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.transform.translate(value = destination, orient_type = 'GLOBAL')
        bpy.ops.object.mode_set(mode = 'OBJECT')
       

def extrude(face):
    
    # Extrudes by 0
    bpy.ops.object.select_all(action = 'DESELECT')
    
    bpy.context.view_layer.objects.active = mol
    mol.select_set(True)
    
    mol.data.polygons.active = face
    mol.data.polygons[face].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0)})
    bpy.ops.object.mode_set(mode='OBJECT')
    
def flip():

    # Flips the mesh
    if closed:
        index = 1
    else:
        index = 0
        
    for vert in cur.data.vertices[:-1]:
        index += 1
        if closed:
            if index == 2:
                normal = (cur.data.vertices[0].co.copy() - cur.data.vertices[verticeCountCur - 1].co.copy()).normalized().to_4d()
            else:
                normal = (cur.data.vertices[index - 2].co.copy() - cur.data.vertices[index - 3].co.copy()).normalized().to_4d()
        else:
            normal = (cur.data.vertices[index].co.copy() - cur.data.vertices[index - 1].co.copy()).normalized().to_4d()
            
        normal.w = 0
        BA = (mwCur @ normal).to_3d()
        
        if closed:
            
            if index > 2:
                if prev != BA:
                    break
        else:
            if index > 1:
                if prev != BA:
                    break
    
        prev = BA
    
    if closed:
        normal2 = (cur.data.vertices[0].co - cur.data.vertices[verticeCountCur - 1].co).normalized().to_4d()
        
    else:
        normal2 = (cur.data.vertices[1].co - cur.data.vertices[0].co).normalized().to_4d()
        
    BA.normalize()
    
    normal2.w = 0
    vec = (mwCur @ normal2).to_3d()
    vec.normalize()
    
    upcross = BA.cross(vec)
    upcross.normalize()
    
    sidecross = upcross.cross(vec)
    
    sidecross.normalize()
    
    select(0)
    
    bpy.ops.transform.resize(center_override = (mwMol @ mol.data.vertices[VertIndex].co), value = Vector((1, -1, 1)), orient_matrix = (vec, sidecross, upcross))
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
def rotateface(f, origin):

    # Aligns the face to point upwards
    if closed:
        normal2 = (cur.data.vertices[0].co - cur.data.vertices[verticeCountCur - 1].co).normalized().to_4d()
        normal2.w = 0
        vec = (mwCur @ normal2).to_3d()
        vec.normalize()
        
        index = 0
        
        for vert in cur.data.vertices[:-1]:
            index += 1
        
            normal = (cur.data.vertices[index].co.copy() - cur.data.vertices[index - 1].co.copy()).normalized().to_4d()
            normal.w = 0
            BA = (mwCur @ normal).to_3d()
        
            if BA != vec:
                BA.normalize()
                break
    
    else:
        index = 0
        for vert in cur.data.vertices[:-1]:
            index += 1
        
            normal = (cur.data.vertices[index].co.copy() - cur.data.vertices[index - 1].co.copy()).normalized().to_4d()
            normal.w = 0
            BA = (mwCur @ normal).to_3d()
        
            if index > 1:
                if prev != BA:
                    BA.normalize()
                    break
        
            prev = BA
            
        normal2 = (cur.data.vertices[1].co - cur.data.vertices[0].co).normalized().to_4d()
        normal2.w = 0
        vec = (mwCur @ normal2).to_3d()
        vec.normalize()
        
    cross = BA.cross(vec)
    
    normalFD = (mol.data.vertices[f].co - mol.data.vertices[origin].co).normalized().to_4d()
    normalFD.w = 0
    FD = (mwMol @ normalFD).to_3d()
    
    BA.normalize()
    cross.normalize()
    FD.normalize()
    
    rd = FD.rotation_difference(cross)
    angle = rd.angle

    mat = mathutils.Matrix.Rotation(angle, 4, vec)
        
    if FD.dot(BA) <= 0:
        mol.rotation_euler = (mat @ mol.rotation_euler.to_matrix().to_4x4()).to_euler()
    else:
        mol.rotation_euler = (mat.inverted() @ mol.rotation_euler.to_matrix().to_4x4()).to_euler()

def moveMesh():

    # Turns the curve object into a curve and back to a mesh to refresh indexes
    objs = [cur, ]
    
    bpy.ops.object.convert({"selected_editable_objects": objs}, target='CURVE', keep_original= False)
    bpy.ops.object.convert({"selected_editable_objects": objs}, target='MESH', keep_original= False)

    # Moves origin to VertIndex
    saved_location = bpy.context.scene.cursor.location.copy()
    
    bpy.context.scene.cursor.location = mwMol @ mol.data.vertices[VertIndex].co.copy()
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Moves mold to curve
    if closed:
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = cur
        cur.select_set(True)
        
        deselect(cur)
        cur.data.edges[edgeCount - 1].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        mol.location = bpy.context.scene.cursor.location
        bpy.context.scene.cursor.location = saved_location
        
    else:
        mol.location = mwCur @ cur.data.vertices[0].co.copy()
        
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
def shear(ba, face, fb, rotation):

    # Shears the face in a specific direction
    normal = (cur.data.vertices[int(ba.x)].co.copy()) - (cur.data.vertices[int(ba.y)].co.copy())
    normalBA = normal.normalized().to_4d()
    normalBA.w = 0
    BA = (mwCur @ normalBA).to_3d()
    
    normalvec = (cur.data.vertices[int(ba.x - 1)].co) - (cur.data.vertices[int(ba.y) - 1].co)
    normalvec = normalvec.normalized().to_4d()
    normalvec.w = 0
    vec = (mwCur @ normalvec).to_3d()
    
    normalb2 = (mol.data.vertices[int(fb.x)].co) - (mol.data.vertices[int(fb.y)].co)
    normalFD2 = normalb2.normalized().to_4d()
    normalFD2.w = 0
    FD2 = (mwMol @ normalFD2).to_3d()
    
    BA.normalize()
    vec.normalize()
    FD2.normalize()
    
    mat = mathutils.Matrix.Rotation(math.radians(rotation), 4, vec)
    
    if closed: 
        FD = mat @ FD2
    else:
        FD = mat.inverted() @ FD2
   
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    FD.normalize()

    cross = vec.cross(FD)
    cross.normalize()

    rdFB = vec.rotation_difference(BA)

    angle = math.degrees(rdFB.angle)
    
    if vec.x - BA.x < margin and vec.x - BA.x > -margin and vec.y - BA.y < margin and vec.y - BA.y > -margin and vec.z - BA.z > -margin and vec.z - BA.z < margin:
        direction = "forward"
        
    elif vec.x + BA.x < margin and vec.x + BA.x > -margin and vec.y + BA.y < margin  and vec.y + BA.y > -margin and vec.z + BA.z > -margin and vec.z + BA.z < margin:
        direction = "backward"
        
    elif cross.dot(BA) > 0 and not BA.dot(FD) > margin and not BA.dot(FD) < -margin:
        direction = "right"
        executeShear(fb, vec, cross, face, FD, angle, direction)
        
    elif cross.dot(BA) < 0 and not BA.dot(FD) > margin and not BA.dot(FD) < -margin:
        direction = "left"
        executeShear(fb, vec, cross, face, FD, angle, direction)
        
    elif BA.dot(FD) < 0 and not cross.dot(BA) > margin and not cross.dot(BA) < -margin:
        direction = "up"
        executeShear(fb, vec, cross, face, FD, angle, direction)
        
    elif BA.dot(FD) > 0 and not cross.dot(BA) > margin and not cross.dot(BA) < -margin:
        direction = "down"
        executeShear(fb, vec, cross, face, FD, angle, direction)
        
    else:
        pass
        # print("Multi angle cuts not supported.")
        
def flipNormals():

    # Flips the normals
    select(0)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    mol.data.polygons[0].flip()
    bpy.ops.object.mode_set(mode = 'EDIT')
    
def turn_face_to_point(face, curveIndex, origin):

    # Transform the face to world space to take non-uniform scaling into account
    # Which may change the angle of face.normal
    for index in mol.data.polygons[face].vertices:
        vert = mol.data.vertices[index]
        vert.co = mwMol @ vert.co

    # Get the rotation difference
    track  = (mwCur @ cur.data.vertices[curveIndex].co.copy()) - mol.data.vertices[origin].co.copy()
    q = mol.data.polygons[face].normal.rotation_difference(track)
         
    # Compose the matrix
    # Rotation around origin in world space 
    mat = Matrix.Translation(mol.data.vertices[origin].co.copy()) @ \
          q.to_matrix().to_4x4() @ \
          Matrix.Translation(-mol.data.vertices[origin].co.copy())
         
    # Transform the face back to object space afterwards
    mat_mol = mwMol.inverted() @ mat

    # Apply the matrix to the vertices of the face
    for index in mol.data.polygons[face].vertices:
        vert = mol.data.vertices[index]
        vert.co = mat_mol @ vert.co
        
def rotation(self, context):

    # Rotates the mesh
    rotateface(other, VertIndex)
    
    if closed:
        normal2 = (cur.data.vertices[verticeCountCur - 1].co - cur.data.vertices[0].co).normalized().to_4d()
    else:
        normal2 = (cur.data.vertices[1].co - cur.data.vertices[0].co).normalized().to_4d()
    normal2.w = 0
    vec = (mwCur @ normal2).to_3d()
    vec.normalize()
    
    angle = math.radians(self.degrees)
 
    mat = mathutils.Matrix.Rotation(angle, 4, vec)
    
    mol.rotation_euler = (mat @ mol.rotation_euler.to_matrix().to_4x4()).to_euler()
    
def getScale(self):
    return self.get("scale_factor", 1)
    
def setScale(self, value):
    
    prev_sf = self.get("scale_factor", 1)
    sf = value / prev_sf
    self.scale.xyz *= sf
    self["scale_factor"] = value
    
def checkFlipped():
    
    # Checks if the normal of the mesh points in or not
    if closed:
         normal2 = (cur.data.vertices[0].co - cur.data.vertices[verticeCountCur - 1].co).normalized().to_4d()
    else:
        normal2 = (cur.data.vertices[1].co - cur.data.vertices[0].co).normalized().to_4d()
    normal2.w = 0
    vec = (mwCur @ normal2).to_3d()
    vec.normalize()
    
    for index in mol.data.polygons[0].vertices:
        vert = mol.data.vertices[index]
        vert.co = mwMol @ vert.co
    
    if mol.data.polygons[0].normal.x - vec.x < margin and mol.data.polygons[0].normal.x - vec.x > -margin and mol.data.polygons[0].normal.y - vec.y < margin and mol.data.polygons[0].normal.y - vec.y > -margin and mol.data.polygons[0].normal.z - vec.z < margin and mol.data.polygons[0].normal.z - vec.z > -margin:
        for index in mol.data.polygons[0].vertices:
            vert = mol.data.vertices[index]
            vert.co = mwMol.inverted() @ vert.co
        
        return False
    
    else:
        
        for index in mol.data.polygons[0].vertices:
            vert = mol.data.vertices[index]
            vert.co = mwMol.inverted() @ vert.co
        return True
    
def resetSelection():
    
    # Just resets the selections. May break stuff if you don't do this
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    select(0)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
def initalize():
        
    global mol
    global cur
    global verticeCount
    global verticeCountCur
    global VertIndex
    global other
    global margin
    global edgeCount
    global closed
    global mwCur
    global mwMol
    global autoMerge
    
    # Active
    mol = bpy.context.view_layer.objects.active # Active
    object = [mol, ]

    # Selected
    for o in bpy.context.selected_objects:
        if bpy.context.view_layer.objects.active != o:
            cur = o 
        
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = mol
    mol.select_set(True)
    
    # Getting vertex and edge count of the objects
    verticeCount = 0
    for v in mol.data.vertices:
        verticeCount += 1
    
    verticeCountCur = 0
    for v in cur.data.vertices:
        verticeCountCur += 1
        
    edgeCount = 0
    for edge in cur.data.edges:
        edgeCount += 1
        
    closed = False
    if edgeCount == verticeCountCur:
        closed = True
        
    VertIndex = 0 # d
    other = 1 # f
    margin = .0001
    
    # Assigning matrixes
    mwCur = cur.matrix_world
    mwMol = mol.matrix_world
    
    autoMerge = bpy.context.scene.tool_settings.use_mesh_automerge
    
class loop_operator(bpy.types.Operator):
    """Turns the mesh into a molding using a curve"""
    bl_idname = "mesh.mold_to_curve"
    bl_label = "Molding from mesh"

    def execute(self, context):
        
        if checkFlipped():
            flipNormals()
            if closed:
                loopClosed(bpy.context.scene.degrees)
            else:
                loopOpen(bpy.context.scene.degrees)
  
        else:
            if closed:
                loopClosed(bpy.context.scene.degrees)
            else:
                loopOpen(bpy.context.scene.degrees)
                
        if autoMerge:
            bpy.context.scene.tool_settings.use_mesh_automerge = True
 
        return {'FINISHED'}
    
class flip_operator(bpy.types.Operator):
    """Flips the mesh"""
    bl_idname = "mesh.flip_mold"
    bl_label = "Flip mesh"

    def execute(self, context):
        
        flip()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        if context.scene.get("degrees") is not None:
            context.scene.degrees = 360.0 - context.scene.get("degrees")
 
        return {'FINISHED'} 

class begin_operator(bpy.types.Operator):
    """Must have two objects selected with the mesh as the active"""
    bl_idname = "mesh.begin_operator"
    bl_label = "Move mesh to curve"
    
    def execute(self, context):
    
        bpy.context.scene.property_unset("degrees")
        
        try:
            initalize()
        except:
            self.report({"ERROR"}, "Select the curve, then shift select the mesh")
            return{'CANCELLED'}
        
        resetSelection()
    
        if autoMerge:
            bpy.context.scene.tool_settings.use_mesh_automerge = False
        
        moveMesh()
        
        if closed:
            turn_face_to_point(0, 0, VertIndex)
        else:
            turn_face_to_point(0, 1, VertIndex)
            
        rotateface(other, VertIndex)
        
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.context.view_layer.objects.active = mol
        mol.select_set(True)
        
        
        return {'FINISHED'}
    
class VIEW3D_PT_mesh_to_curve(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type= 'UI'
    bl_category = "Create"
    bl_label = "Mold to Curve"
    
    def draw(self, context):
        
        layout = self.layout
        
        layout.label(text = 'Select the curve')
        layout.label(text = 'Then shift select the mesh')
        
        row = layout.row()
        row.scale_y = 2.5
    
        row.operator('mesh.begin_operator') 
     
        row = layout.row()
        col = row.split().row().box()

        if context.active_object is None:
            layout.label(text = 'Must have an active object')
        else:
            col.prop(context.object, "scale_factor")
     
        row = layout.row()
        col.prop(context.scene, 'degrees', slider = True)
        col.scale_y = 1.1
        
        col.operator('mesh.flip_mold')

        row.scale_y = 1.5
        row.operator('mesh.mold_to_curve')
   
def register():
    
    bpy.utils.register_class(begin_operator)
    bpy.utils.register_class(loop_operator)
    bpy.utils.register_class(flip_operator)
    bpy.utils.register_class(VIEW3D_PT_mesh_to_curve)  
    bpy.types.Scene.degrees = bpy.props.FloatProperty(name='Rotate mesh', soft_min = 0, soft_max = 360, update = rotation)
    bpy.types.Object.scale_factor = bpy.props.FloatProperty(name = 'Scale mesh', default = 1, soft_min = .01, get=getScale, set=setScale)
            
def unregister():
    
    bpy.utils.unregister_class(begin_operator)
    bpy.utils.unregister_class(loop_operator)
    bpy.utils.unregister_class(flip_operator)
    bpy.utils.unregister_class(VIEW3D_PT_mesh_to_curve)
    del bpy.types.Scene.degrees
    del bpy.types.Object.scale_factor

if __name__ == '__main__':
    register()