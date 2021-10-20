---
title: Topological operations on meshes via SMT
theme: white
---

# Transforming cell complexes via SMT

Daniel Shapero

2021 November 8

---

### My day job

----

### Everyone's least favorite task

![Larsen](larsen.png)

----

### Everyone's least favorite task

1. Digitize glacier outline manually in a GIS
2. Transform the outline file into the mesh generator's input format
3. Run the mesh generator
4. Run your simulation
5. Realize your data is goofed up, go to 1.
6. Realize your resolution is poor, go to 3.

----

### Meshing

* Meshing is a huge bottleneck.
* The quality of the mesh affects how well finite element approximations work.
  - Small angles $\Rightarrow$ bad condition number
  - Large angles $\Rightarrow$ bad interpolation error
* All simulation workflows should be adaptive.

---

# Delaunay triangulation

----

### Delaunay triangulation

* The **circumsphere** of a simplex is the unique sphere passing through all its points.
* A **Delaunay triangulation** has the property that **the circumsphere of every simplex is empty**.

----

### Empty circumcircles

![Full circumcircles](drawing1.svg) ![Empty circumcircles](drawing2.svg)

Triangulation of two cells; left is not Delaunay, right is

----

### A key property

Among all triangulations of a point set, the Delaunay triangulation **maximizes** the **minimum** angle.

----

### Algorithms

There are two basic types of algorithms in 2D:
* edge flipping
* polygon retriangulation

----

### Aren't we done?

* We started with just the boundary $\partial\Omega$.
* We also need to:
  1. Fill in the points in the interior
  2. Constrain the triangulation to include $\partial\Omega$
* Filling interior points is half the challenge.

----

### What about 3D?

* Things get much worse in 3D because of *slivers*.
* Enforcing the empty circumsphere property alone doesn't guarantee you a good triangulation.
* There are 3D piecewise linear complexes with no tetrahedralization.

----

### Things people work on

* Better internal insertion algorithms in 2D
* Evaluating geometric kernels in floating point
* Everything goes to hell in 3D, how to recover?
* Quad and hex meshing
* Meshing curved geometries
* Correcting broken or degenerate topologies

---

All of those are fine but can we talk about how awful the basic kernels are to write in the first place?

----

Just flipping a triangle edge is surprisingly hard.

![flips](https://upload.wikimedia.org/wikipedia/commons/d/dc/Flips2d3d.svg)

In 3D things become truly heinous.
3-2 and 2-3 flips are far from the worst of it too!

<small>From <a href="https://en.wikipedia.org/wiki/Flip_graph">flip graph</a> wiki page</small>

----

### Desiderata

* Lots of literature focuses only on simplices.
I want cubical or polygonal complexes too!
* Ordering only gives orientation for simplices.
