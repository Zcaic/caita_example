from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import Part, PartDocument
from pycatia.product_structure_interfaces.product_document import Product, ProductDocument
from pycatia.in_interfaces.reference import Reference
from pycatia.hybrid_shape_interfaces.point import Point

import aerosandbox as asb
import numpy as np
from pathlib import Path

def init():
    caa = catia()
    doc: PartDocument = caa.documents.item("wing.CATPart")
    doc = PartDocument(doc.com_object)
    part:Part = doc.part

    hsf=part.hybrid_shape_factory
    
    hb=part.hybrid_bodies.add()
    hb.name="baseline"
    selection=doc.selection
    selection.clear()

    #--------------------------------------------root------------------------------------
    root_af=asb.KulfanAirfoil("ls417").set_TE_thickness(thickness=2.4e-3)
    root_spline=hsf.add_new_spline()
    root_spline.name="root_spline"
    root_scaler=751.2
    for i,iv in enumerate(root_af.to_airfoil(n_coordinates_per_side=100).coordinates*root_scaler):
        pt=hsf.add_new_point_coord(iv[0],0.0,iv[1])
        pt.name=f"root_{i}"
        hb.append_hybrid_shape(pt)
        selection.add(pt)
        root_spline.add_point(pt)
    hb.append_hybrid_shape(root_spline)
    part.in_work_object=root_spline
    selection.vis_properties.set_show(1)
    selection.clear()
    #----------------------------------------------------------------------------------------
    
    #-------------------------------------------tip----------------------------------------------
    tip_af=asb.KulfanAirfoil("ls417").set_TE_thickness(thickness=2.4e-3)
    tip_spline=hsf.add_new_spline()
    tip_spline.name="tip_spline"
    tip_scaler=751.2
    for i,iv in enumerate(tip_af.to_airfoil(n_coordinates_per_side=100).coordinates*tip_scaler):
        pt=hsf.add_new_point_coord(iv[0],4790.85,iv[1])
        pt.name=f"tip_{i}"
        hb.append_hybrid_shape(pt)
        selection.add(pt)
        tip_spline.add_point(pt)
    hb.append_hybrid_shape(tip_spline)
    part.in_work_object=tip_spline
    selection.vis_properties.set_show(1)
    selection.clear()

    #-------------------------------------------------------------------------------------------
    part.update()
    
def parameterize():
    caa=catia()
    doc=caa.documents.item("wing.CATPart")
    doc=PartDocument(doc.com_object)
    part=doc.part
    main_wing=part.hybrid_bodies.item("main_wing")
    tip_le:Point=main_wing.hybrid_shapes.item("tip_le")
    tip_le=Point(tip_le.com_object)
    base_coords=np.array(tip_le.get_coordinates())
    modify_coords=base_coords+np.array([1000.0,0.0,0.0])
    tip_le.set_coordinates(modify_coords)
    print(modify_coords)

    part.update()

    prodocument=caa.active_document
    prodocument.export_data(Path("./xxx/xxx.stp").resolve().as_posix(),"stp",overwrite=True)

if __name__ == "__main__":
    # init()
    parameterize()
