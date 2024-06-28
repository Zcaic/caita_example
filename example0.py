from pycatia import catia
from pycatia.mec_mod_interfaces.part import Part
from pycatia.mec_mod_interfaces.body import Body
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.in_interfaces.reference import Reference
from pycatia.hybrid_shape_interfaces.point import Point

import aerosandbox as asb
import numpy as np
from pathlib import Path

def main0():
    caa=catia()
    # caa.visible=False
    doc:PartDocument=caa.documents.add('Part')
    doc=caa.active_document
    part:Part=doc.part
    mb:Body=part.main_body
    mb.name='main_body'

    try:
        rae2822:asb.KulfanAirfoil=asb.Airfoil(name='rae2822').to_kulfan_airfoil(n_weights_per_side=5)
        rae2822_coords=np.zeros((199,3),dtype='f8')
        rae2822_coords[:,[0,2]]=rae2822.to_airfoil(n_coordinates_per_side=100).coordinates*1000

        hsf=part.hybrid_shape_factory
        geom_set=part.hybrid_bodies.add()
        geom_set.name="wing"
        sel=doc.selection
        sel.clear()

        # pt=hsf.add_new_point_coord(*rae2822_coords[0])
        spline=hsf.add_new_spline()
        for i,iv in enumerate(rae2822_coords):
            pt=hsf.add_new_point_coord(*iv)
            pt.name=f"pt{i}"
            pt_ref=Reference(pt.com_object)
            # mb.insert_hybrid_shape(pt)
            geom_set.append_hybrid_shape(pt)
            sel.add(pt)
            spline.add_point(pt_ref)

        # mb.insert_hybrid_shape(spline)
        geom_set.append_hybrid_shape(spline)
        part.in_work_object=spline
        sel.vis_properties.set_show(1)
        
        part.update()

        pt=geom_set.hybrid_shapes.get_item_by_name('pt0')
        pt=Point(pt.com_object)
        print(pt.set_coordinates((1500.0,0.0,0.0)))

        filename=Path("./wing.CATPart").resolve().as_posix()
        doc.save_as(filename,overwrite=True)
    finally:
        doc.close()

if __name__=="__main__":
    main0()

