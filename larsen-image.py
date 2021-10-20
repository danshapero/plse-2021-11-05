import subprocess
import numpy as np
import geojson
import rasterio
import firedrake
import icepack
import matplotlib.pyplot as plt

outline_filename = icepack.datasets.fetch_outline("larsen")
with open(outline_filename, "r") as outline_file:
    outline = geojson.load(outline_file)

coords = np.array(list(geojson.utils.coords(outline)))
image_filename = icepack.datasets.fetch_mosaic_of_antarctica()
with rasterio.open(image_filename, "r") as image_file:
    transform = image_file.transform
    δ = 50e3
    window = rasterio.windows.from_bounds(
        left=coords[:, 0].min() - δ,
        bottom=coords[:, 1].min() - δ,
        right=coords[:, 0].max() + δ,
        top=coords[:, 1].max() + δ,
        width=image_file.width,
        height=image_file.height,
        transform=transform,
    )
    image = image_file.read(indexes=1, window=window, masked=True)
    xmin, ymin, xmax, ymax = rasterio.windows.bounds(window, transform)
    extent = (xmin, xmax, ymin, ymax)

fig, axes = plt.subplots(ncols=3, sharex=True, sharey=True, figsize=(12, 4))
for ax in axes:
    ax.set_aspect("equal")
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.imshow(image, cmap="Greys_r", vmin=12e3, vmax=16.38e3, extent=extent)

for feature in outline["features"]:
    for line_string in feature["geometry"]["coordinates"]:
        xs = np.array(line_string)
        axes[1].plot(xs[:, 0], xs[:, 1], linewidth=0.5)

geometry = icepack.meshing.collection_to_geo(outline)
with open("larsen.geo", "w") as geo_file:
    geo_file.write(geometry.get_code())

subprocess.run("gmsh -2 -format msh2 -v 2 -o larsen.msh larsen.geo".split())
mesh = firedrake.Mesh("larsen.msh")
kwargs = {"interior_kw": {"linewidth": 0.25}, "boundary_kw": {"linewidth": 0.5}}
firedrake.triplot(mesh, axes=axes[2], **kwargs)

fig.savefig("larsen.png", dpi=300, bbox_inches="tight")

with open("larsen-quad.geo", "w") as geo_file:
    geo_file.write(geometry.get_code())
    geo_file.write("\n"
                   "Recombine Surface{s0};\n"
                   "Mesh.SubdivisionAlgorithm = 1;\n"
                   "Mesh.Algorithm = 8;\n")

subprocess.run("gmsh -2 -format msh -v 2 -o larsen-quad.msh larsen-quad.geo".split())
