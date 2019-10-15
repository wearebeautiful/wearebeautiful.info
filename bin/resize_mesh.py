#!/usr/bin/env python

"""
Dumbass mesh scale function
"""
import sys
import os
from time import time
import numpy as np

import pymesh
import click

def resize_mesh(mesh, scale):
    new_faces = []
    for face in mesh.faces:
        new_face = []
        for f in list(face):
            new_face.append(f * scale)

        new_faces.append(new_face)

    return pymesh.form_mesh(mesh.vertices, np.array(new_faces))


@click.command()
@click.argument("scale", nargs=1, type=float)
@click.argument("in_file", nargs=1)
@click.argument("out_file", nargs=1)
def resize(scale, in_file, out_file):

    mesh = pymesh.meshio.load_mesh(in_file)
    mesh = resize_mesh(mesh, scale)
    pymesh.meshio.save_mesh(out_file, mesh)


def usage(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == "__main__":
    print("resize_mesh.py running, silliness im dorf. <3\n")
    resize()
    sys.exit(0)