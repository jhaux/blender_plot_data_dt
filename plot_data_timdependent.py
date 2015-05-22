__author__ = 'Johannes Haux'

import bpy
import numpy as np
import time


#############################
#####     functions     #####
#############################
def cleanup_meshes():
    #unselect everything
    # <insert code here, this can vary depending on your situation> 
    bpy.ops.object.select_all()
    
    # gather list of items of interest.
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

    # select them only.
    for object_name in candidate_list:
        bpy.data.objects[object_name].select = True
    
    # remove all selected.
    bpy.ops.object.delete()
    
    # remove the meshes, they have no users anymore.
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
    
    print(str(__name__) + ':','CLEANUP DONE')
  
  
def scale_to_plotspace(samplespace, samplecoords, plotspace=(40,40,40)):
    factors = [float(plotspace[i]) / float(samplespace[i]) for i in range(3)]
    newcoords = [factors[i] * float(samplecoords[i]) for i in range(3)]
    return newcoords


def rescale_maxsize(samplesize, samplemax, newmax):
    return float(samplesize) * float(newmax) / float(samplemax)


def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
 

def makeMaterial(name, diffuse, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.alpha = alpha
    mat.ambient = 1
    return mat


def load_data(path_to_data):
    all_data = np.genfromtxt(path_to_data, delimiter=' ', skip_header=1)
    X_t = all_data[:, 0::3]
    Y_t = all_data[:, 1::3]
    Z_t = all_data[:, 2::3]
    return X_t, Y_t, Z_t


if __name__ == '__main__':
    time_start = time.time()

    cleanup_meshes()


    path = '/home/johannes/Google Drive/Uni HD/GPU Computing/git_repository/GPU/exercise_7/plot/data/output.csv'
    X_t, Y_t, Z_t = load_data(path)
    masses = np.genfromtxt(path, delimiter=' ', skip_footer=500)
    print(masses)
    print(X_t[0,0])
    print(Y_t[0,0])
    print(Z_t[0,0])
    
    for x,y,z,j in zip(X_t[0], Y_t[0], Z_t[0], range(len(X_t[0]))):
        segs = 32
        rings = 16
        # Step 1: Generate the stars at their positions with size corresponding to radius
        loc = scale_to_plotspace(samplespace=(400,400,400), samplecoords=(x,y,z))
        size = rescale_maxsize(masses[j]**(1./3.), 100**(1./3.), 0.1)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=rings, location=loc, size=size)
        this_sphere = bpy.context.object
        bpy.ops.object.shade_smooth()
        print(this_sphere.name)
        for xx,yy,zz,i in zip(X_t[:,j], Y_t[:,j], Z_t[:,j], range(len(X_t[:,j]))):
            loc = scale_to_plotspace(samplespace=(400,400,400), samplecoords=(xx,yy,zz))
            this_sphere.location[0] = loc[0]
            this_sphere.keyframe_insert(data_path="location", frame=i+1, index=0)
            this_sphere.location[1] = loc[1]
            this_sphere.keyframe_insert(data_path="location", frame=i+1, index=1)
            this_sphere.location[2] = loc[2]
            this_sphere.keyframe_insert(data_path="location", frame=i+1, index=2)



    print("My Script Finished: %.4f sec" % (time.time() - time_start))