# Image Morphing · Geometry to Animation

**Triangulated warping · Affine transforms · Image interpolation · Fall 2026**

## Objective

Produce a continuous transition between two images by interpolating both the **shape** (landmark geometry) and the **appearance** (pixel colors).

## Mathematics

Given corresponding landmarks \(\mathbf p_i^A,\mathbf p_i^B\), the intermediate shape at \(t\in[0,1]\) is

$$\mathbf p_i(t)=(1-t)\mathbf p_i^A+t\mathbf p_i^B.$$

Each corresponding triangle defines a piecewise affine warp. After warping both source images into the intermediate geometry, appearance is interpolated:

$$I_t(\mathbf x)=(1-t)I_A(W_A^{-1}(\mathbf x,t))+tI_B(W_B^{-1}(\mathbf x,t)).$$

This separates **geometric alignment** from **cross-dissolve**; blending without warping would produce ghosting rather than a shape transition.

## Recorded results

| Evidence | Observation |
|---|---|
| Notebook test section | **3/3 tests passed** (as printed by notebook) |
| Animated outputs | **custom1.gif**, **custom2.gif**, **output.gif** supplied |
| Qualitative result | Generated face-morph animations and intermediate rendered images |

The three passing tests are notebook-reported, not an independently rerun test suite. No pixel-error benchmark, frame rate, or user-study metric is recorded.

## Visual presentation

The three original GIFs are retained in the private evidence archive pending permission to publish the underlying photographs and course assets. Their existence is verified; the animations are not silently replaced with stock examples.

[← Computer Vision](../README.md) · [Portfolio index](../../SHOWCASE.md)
