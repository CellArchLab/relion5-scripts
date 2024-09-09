# relion5-scripts
Utility scripts for handling subtomogram STAR files from RELION-5.

## rln5_to_artiax.py

Example usage:

```bash
rln5_to_artiax.py --instar particles.star --outstar particles_artiax.star --x 1024 --y 1024 --z 256
```

## rln5_to_imod.py

Example usage:

```bash
rln5_to_imod.py --instar particles.star --outmod particles_Position_1.mod --tomo Position_1 --angpix 7.84 --x 1024 --y 1024 --z 256
```
