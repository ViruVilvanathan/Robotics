# Poisson Image Editing · Reconstructing Images from Gradients

**Optimization · Discrete Laplacian · Sparse linear systems · Fall 2026**

## Objective

Edit an image by controlling its **spatial gradients**, rather than directly copying source pixel intensities. This makes boundary transitions more consistent with the destination image.

## Mathematics

Inside an editing region \(\Omega\), recover an image \(f\) from a chosen gradient field \(\mathbf v\), with destination boundary conditions:

$$\underset{f}{\min}\int_\Omega\|\nabla f-\mathbf v\|^2\,d\mathbf x,\qquad f|_{\partial\Omega}=f^*|_{\partial\Omega}.$$

The Euler–Lagrange condition gives the Poisson equation:

$$\Delta f=\nabla\cdot\mathbf v.$$

On a four-neighbor pixel grid, the reconstruction becomes a sparse linear system \(A\mathbf f=\mathbf b\).

## Three recorded editing variants

| Variant | Gradient strategy | Submitted output |
|---|---|---|
| **Seamless cloning** | Prefer source gradients within the selected region, constrained by destination boundary | **cloned.png** |
| **Mixed-gradient editing** | Choose source or destination gradient with larger magnitude at each neighbor relation | **mixed.png** |
| **Texture flattening** | Suppress gradients away from retained edges | **flatten.png** |

The submitted notebook includes output images for all three methods. **No PSNR, SSIM, or quantitative perceptual benchmark was recorded**, and no numerical quality score is invented.

## Visual results

### Seamless cloning

![Seamless cloning result](assets/cloned.png)

### Mixed gradients

![Mixed-gradient editing result](assets/mixed.png)

### Texture flattening

![Texture flattening result](assets/flatten.png)

## Why the variants matter

- **Seamless cloning:** transfers an object while accommodating destination illumination and boundary colors.
- **Mixed gradients:** retains strong edges from either image, potentially preserving important scene structure.
- **Texture flattening:** reduces small texture variations while keeping selected salient edges.

## Evidence and publication boundary

Source: uploaded **Fall_2026_CIS5180_Virupakshan_Vilvanathan.ipynb** (filename as submitted), with the three output PNGs. Course affiliation is described as CIS 5810 based on the project context; the notebook filename itself says CIS5180. Only the three selected result images are published here. Instructor-provided code, assignment notebooks, and dataset files are excluded.

[← Computer Vision](../README.md) · [Portfolio index](../../SHOWCASE.md)
