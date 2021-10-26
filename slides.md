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

Among all triangulations of a point set, Delaunay triangulations **maximize** the **minimum** angle.

----

### Algorithms

There are two basic types of algorithms in 2D:
* edge flipping
* polygon retriangulation

----

pictures

----

### Aren't we done?

* We started with just $\partial\Omega$.
We also need to:
  1. Fill points in the interior
  2. Constrain the triangulation to include $\partial\Omega$
* Filling interior points is half the challenge -- Delaunay is best, still might not be good enough.

----

![sliver](sliver.svg)

<small>From <a href="https://people.eecs.berkeley.edu/~jrs/papers/delref3d.pdf">Shewchuk (1998)</a>:
"Tetrahedra with poor angles.
Needles and wedges have edges of greatly disparate length; caps have a large solid angle; slivers have neither, but can have good circumradius-to-shortest edge ratios."
</small>


----

### Things people work on

* Better incremental interior insertion
* Evaluating geometric kernels in floating point
* Fixing sub-optimality of Delaunay in 3D
* Quad and hex meshing
* Meshing curved geometries
* Correcting broken or degenerate topologies

----

### Before we get ahead of ourselves


* Let's look at some code for transforming the topology of a triangulation:
    * [TTL](https://github.com/SINTEF-Geometry/TTL/blob/49ff0dbabefccb55b1f5793dab2ffcda1cb4da7d/src/halfedge/HeTriang.cpp#L542)
    * [CGAL](https://github.com/CGAL/cgal/blob/ed3503d2381842f837a8118a749ab380f889485b/Triangulation_2/include/CGAL/Regular_triangulation_2.h#L1629)
    * [gmsh](https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/Mesh/meshGFaceDelaunayInsertion.cpp#L1901)
    * [TriWild](https://github.com/wildmeshing/TriWild/blob/d85ec7a6faf50138c034a174226515b44d345c03/src/triwild/edge_swapping.cpp#L54)
    * [garbage](https://gitlab.com/danshapero/zmsh2/-/blob/delaunay/src/algorithms/delaunay.c#L52) by me
* How does this code make you feel?

----

Flipping an edge is surprisingly hard.

![flips](https://upload.wikimedia.org/wikipedia/commons/d/dc/Flips2d3d.svg)

3D transformations are harder: 3 $\leftrightarrow$ 2 face flips...

<small>From <a href="https://en.wikipedia.org/wiki/Flip_graph">flip graph</a> wiki page</small>

----

...but those are far from the worst of it!

![transformations](topological-transformations.svg)

<small>From <a href="https://doi.org/10.1007/978-3-540-75103-8_1">Klingner and Shewchuk (2008)</a></small>

----

**Topological transformation kernels are heinous.**

Can we make them nicer to look at and write?

----

### Desiderata

* Lots of literature focuses only on simplices in 2D or 3D.
I want cubical or polyhedral complexes!
* Ordering only gives orientation for simplices.
No more half-edge or winged edge data structures.
* Less imperative, more declarative.

---

# Homological algebra

----

* All the data structures for meshes describe adjacency.
They also need is *orientation*.
* The simplest case: an edge $e$ goes from $v_0$ to $v_1$.
* We can write that
$$\partial e = v_1 - v_0.$$

----

* Just like we can "add" vertices, we can "add" edges two and extend by linearity.
* Suppose $e_0 = v_1 - v_0$, $e_1 = v_2 - v_1$.
Then
$$\partial(e_0 + e_1) = v_2 - v_0,$$
and likewise
$$\partial(e_1 - e_0) = v_2 - 2v_1 + v_0.$$

----

* Suppose a triangle $t$ has edges $e_0$, $e_1$, $e_2$ and is positively-oriented w.r.t. all of them.
We can likewise say that
$$\partial t = e_0 + e_1 + e_2.$$
* Suppose that $e_1$ had its orientation flipped.
We'd then have that
$$\partial t = e_0 - e_1 + e_2.$$
Orientation of each cell is immaterial.

----

### Definitions

* Let $X_k$ be all the cells of dimension $k$.
* The $k$-*chains* $C_k$ are the set of all integer linear combinations of elements of $X_k$.
* $\partial_k : C_k \to C_{k - 1}$ is a linear operator.

----

* For a nice mesh, topological and geometric orientation should agree.
* If the vertices of each of these two triangles are ordered positively, the two points they have in common will appear in the opposite order w.r.t. each other.

----

Neighboring top cells should have opposite orientation w.r.t. their common boundary cells.

----

$$\Huge{\partial_k\circ\partial_{k + 1} = 0}$$

----

pictures

----

### An annoying problem

* $\partial\circ\partial = 0$ is useful, but what prevents us from having an edge $e$ such that
$$\partial e = v_1 + v_0?$$
* We could impose this as an extra side condition.

----

### Some convenient fictions

* Or, we could say that there is a cell $\bot$ of dimension -1 such that, for all $k$,
$$\partial v_k = \bot$$
* The vertex boundary matrix is a row of 1s!
* If we did have $\partial e = v_1 + v_0$, then
$$\partial_0\circ\partial_1e = 2\bot \neq 0!$$

----

### Homology

* If $\alpha$ is a boundary, it has no boundary.
* Are there chains that have zero boundary, but that are not themselves boundaries?
* These chains constitute the **homology groups**:
$$H_k = \text{kernel }\partial_k / \text{image }\partial_{k + 1}$$

----

torus image

----

### Categories

* To every (reasonable) *topological space* you can associate a *group*.
* This is profoundly disturbing and gets us in Russell's paradox territory.
* This is why people came up with category theory.
* "I'd like to learn to ~~play~~ math like that, and then not do it." ~Frank Proffitt

----

### A data structure

* We can represent cell complexes as a bunch of **sparse matrices** with **integer entries**.
* How convenient that scipy, eigen or plenty of other packages give us this.

----

### Linear algebra

* This interpretation opens up all sorts of linear algebraic reasoning to us.
* For example, to merge two cells $t_0$ and $t_1$, we replace those columns in the boundary matrix with $\partial(t_0 + t_1)$.
* Suppose that $P$, $Q$ are matrices such that $PQ = \rho I$ for some integer $\rho$.
Then
$$0 = \rho\cdot\partial_k\circ\partial_{k + 1} = (\partial_k \circ P)\circ(Q\circ\partial_{k + 1})$$


----

![meme](linear-algebra.jpg)

----

### Ordering

* Data structures for simplexes (e.g. half-edge) often assume consistent ordering, which implies:
  - good input data
  - manifold topology
* Remember that there are non-Hamiltonian polyhedra: [Tutte](https://en.wikipedia.org/wiki/Tutte_graph), [Herschel](https://en.wikipedia.org/wiki/Herschel_graph), [Goldner-Harary](https://en.wikipedia.org/wiki/Goldner%E2%80%93Harary_graph).
* Moral: orientation good, ordering bad.

---

# Transforming topologies

----

### Joining cells

* Using linear algebra makes implementing certain transformations really easy.
* Ex: join two triangles into a quadrilateral = add their columns in the boundary matrix.

----

picture

---

# Closing thoughts

----

This representation of cell complexes:
* Is easy to check for correctness
* Is independent of the intrinsic dimension
* Is independent of the coordinate number (simplex, cubical, polyhedral)
* Allows a rich set of transformations to be implemented easily and declaratively

----

### Parallelism

* All of this was very single-threaded.
* For real PDE problems, we decompose the domain and go parallel.
* We can treat the domains and the interfaces between them as a higher-level cell complex.

----

### Some mesh generators

* [Triangle](https://www.cs.cmu.edu/~quake/triangle.html), [aCute](https://www.cise.ufl.edu/~ungor/aCute/), [tetgen](https://tetgen.org)
* [TriWild](https://github.com/wildmeshing/TriWild), [TetWild](https://github.com/wildmeshing/fTetWild)
* [gmsh](https://gmsh.info)
