#!/usr/bin/env python

"""
Remesh the input mesh to remove degeneracies and improve triangle quality.
"""
import sys
import os
from time import time
import argparse
import numpy as np
from numpy.linalg import norm

import pymesh

def fix_mesh(mesh, target_len):
    bbox_min, bbox_max = mesh.bbox;
    diag_len = norm(bbox_max - bbox_min);

    count = 0;
    print("  remove degenerated triangles")
    mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100);
    print("  split long edges")
    mesh, __ = pymesh.split_long_edges(mesh, target_len);
    num_vertices = mesh.num_vertices;
    while True:
        print("  pass %d" % count)
        print("    collapse short edges #1")
        mesh, __ = pymesh.collapse_short_edges(mesh, 1e-6);
        print("    collapse short edges #2")
        mesh, __ = pymesh.collapse_short_edges(mesh, target_len,
                preserve_feature=True);
        print("    remove obtuse triangles")
        mesh, __ = pymesh.remove_obtuse_triangles(mesh, 150.0, 100);
        if mesh.num_vertices == num_vertices:
            break;

        print("  %d of %s vertices." % (num_vertices, mesh.num_vertices))

        num_vertices = mesh.num_vertices;
        count += 1;
        if count > 10: break;

    print("  resolve self intersection")
    mesh = pymesh.resolve_self_intersection(mesh);
    print("  remove duplicated faces")
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    print("  computer outer hull")
    mesh = pymesh.compute_outer_hull(mesh);
    print("  remove duplicated faces")
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    print("  remove obtuse triangles")
    mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5);
    print("  remove isolated vertices")
    mesh, __ = pymesh.remove_isolated_vertices(mesh);

    return mesh;


def parse_args():
    parser = argparse.ArgumentParser(
            description=__doc__);
    parser.add_argument("--timing", help="print timing info",
            action="store_true");
    parser.add_argument("--len", help="target lenght of segments to preserve", type=float)
    parser.add_argument("in_mesh", help="input mesh");
    parser.add_argument("out_mesh", help="output mesh");
    return parser.parse_args();


def scale_mesh(in_file, out_file, target_len):
    mesh = pymesh.meshio.load_mesh(in_file);
    mesh = fix_mesh(mesh, target_len);
    pymesh.meshio.save_mesh(out_file, mesh);

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: scale_mesh.py <len> <src dir> <dest dir>")
        sys.exit(-1)

    len = float(sys.argv[1])
    src_dir = sys.argv[2]
    dest_dir = sys.argv[3]

    for filename in os.listdir(src_dir):
        if filename.lower().endswith(".stl") or filename.lower().endswith(".obj"):
            print("%s -> %.2f" % (filename, len))
            t0 = time()
            scale_mesh(os.path.join(src_dir, filename), os.path.join(dest_dir, filename), len)
            print("  done with file. %d seconds elapsed.\n" % (time() - t0))

    print("\ndone with all files.")