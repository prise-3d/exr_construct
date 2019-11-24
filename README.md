# exr_construct

## description
This program generates an exr image from the average of an exr file set.
It can also calculate intermediate files.

## dependencies
- numpy
- OpenEXR


## usage

```
usage: exr_construct.py [-h] [-s STEP] [-o OUTPUT] [-i INTERVAL] [-I] path

positional arguments:
  path

optional arguments:
  -h, --help            show this help message and exit
  -s STEP, --step STEP  step used for rendering
  -o OUTPUT, --output OUTPUT
                        output directory
  -i INTERVAL, --interval INTERVAL
                        interval for intermediate files (must be a multiple of
                        step)
  -I, --intermediate    compute intermediate exr files
```

## usage example

python exr_construct.py -s 10 -o png/ -i 50 -I exr/
