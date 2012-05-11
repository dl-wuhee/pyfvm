#! /usr/bin/env python
# -*- coding: utf-8 -*-
import voropy
import numpy as np
import time
# ==============================================================================
def _main():

    # get the file name to be written to
    args = _parse_options()

    # dimensions of the rectangle
    cc_radius = 5.0 # circumcircle radius
    lx = np.sqrt(2.0) * cc_radius
    l = [lx, lx]

    # corner points
    points = [ ( -0.5*l[0], -0.5*l[1] ),
               (  0.5*l[0], -0.5*l[1] ),
               (  0.5*l[0], 0.0 ),
               (  0.0, 0.0 ),
               (  0.0, 0.5*l[1] ),
               ( -0.5*l[0],  0.5*l[1] ) ]

    print 'Creating mesh...',
    start = time.time()
    import meshpy.triangle
    info = meshpy.triangle.MeshInfo()
    info.set_points( points )
    def _round_trip_connect(start, end):
        result = []
        for i in xrange(start, end):
            result.append((i, i+1))
        result.append((end, start))
        return result
    info.set_facets(_round_trip_connect(0, len(points)-1))
    def _needs_refinement(vertices, area):
        return bool(area > args.maxarea)
    meshpy_mesh = meshpy.triangle.build(info,
                                        refinement_func = _needs_refinement
                                        )
    mesh = voropy.mesh2d(meshpy_mesh.points, meshpy_mesh.elements)
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    num_nodes = len(mesh.node_coords)
    print '\n%d nodes, %d elements\n' % (num_nodes, len(mesh.cells))

    # write the mesh
    print 'Writing mesh...',
    start = time.time()
    mesh.write( args.filename )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    return
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser( description = 'Construct a triangulation of an L-shaped domain.' )


    parser.add_argument( 'filename',
                         metavar = 'FILE',
                         type    = str,
                         help    = 'file to be written to'
                       )

    parser.add_argument( '--maxarea', '-m',
                         metavar = 'MAXAREA',
                         dest='maxarea',
                         nargs='?',
                         type=float,
                         const=1.0,
                         default=1.0,
                         help='maximum triangle area of the triangulation (default: 1.0)'
                       )

    return parser.parse_args()
# ==============================================================================
if __name__ == "__main__":
    _main()
# ==============================================================================
