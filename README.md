# ply_to_splat
A Python funtion/script to convert Gaussian Splatting .ply files to .splat files.
The .splat file is a compressed representation so as part of this conversion all information about spherical harmonics and accordingly view-dependent effects is lost.

This is usable as a script through setting the "ply_file_to_convert" and "output_filename" variables or through importing the function and using it yourself.

The dependencies are numpy and <a href="https://github.com/dranjan/python-plyfile">plyfile</a>.
