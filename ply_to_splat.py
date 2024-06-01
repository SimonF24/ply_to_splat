import numpy as np
from plyfile import PlyData

ply_file_to_convert = "splat.ply"
output_filename = "splat.splat"

def sh2rgb(sh: list[float]) -> np.ndarray:
    """
    Converts from 0th order spherical harmonics to rgb [0, 255]
    """
    C0 = 0.28209479177387814
    rgb = [sh[i] * C0 + 0.5 for i in range(len(sh))]
    return np.clip(rgb, 0, 1) * 255


def convert_ply_to_splat(input_ply_filename: str, output_splat_filename: str) -> None:
    """
    Converts a provided .ply file to a .splat file. As part of this all information on
    spherical harmonics is thrown out, so view-dependent effects are lost
    
    Args:
        input_ply_filename: The path to the .ply file that we want to convert to a .splat file
        output_splat_filename: The path where we'd like to save the output .splat file
    Returns:
        None
    """

    plydata = PlyData.read(input_ply_filename)
    with open(output_splat_filename, "wb") as splat_file:
        for i in range(plydata.elements[0].count):
            # Ply file format
            # xyz Position (Float32)
            # nx, ny, nz Normal vector (Float32) (for planes, not relevant for Gaussian Splatting)
            # f_dc_0, f_dc_1, f_dc_2 "Direct current" (Float32) first 3 spherical harmonic coefficients
            # f_rest_0, f_rest_1, ... f_rest_n "Rest" (Float32) of the spherical harmonic coefficients
            # opacity (Float32)
            # scale_0, scale_1, scale_2 Scale (Float32) in the x, y, and z directions
            # rot_0, rot_1, rot_2, rot_3 Rotation (Float32) Quaternion rotation vector
            
            # Splat file format
            # XYZ - Position (Float32)
            # XYZ - Scale (Float32)
            # RGBA - Color (uint8)
            # IJKL - Quaternion rotation (uint8)
            
            plydata_row = plydata.elements[0][i]
            
            # Position
            splat_file.write(plydata_row['x'].tobytes())
            splat_file.write(plydata_row['y'].tobytes())
            splat_file.write(plydata_row['z'].tobytes())
            
            # Scale
            for i in range(3):
                splat_file.write(np.exp(plydata_row[f'scale_{i}']).tobytes())
            
            # Color
            sh = [plydata_row[f"f_dc_{i}"] for i in range(3)]
            rgb = sh2rgb(sh)
            for color in rgb:
                splat_file.write(color.astype(np.uint8).tobytes())
                
            opac = 1.0 + np.exp(-plydata_row['opacity'])
            opacity = np.clip((1/opac) * 255, 0, 255)
            splat_file.write(opacity.astype(np.uint8).tobytes())
            
            # Quaternion rotation
            rot = np.array([plydata_row[f"rot_{i}"] for i in range(4)])
            rot = np.clip(rot * 128 + 128, 0, 255)
            for i in range(4):
                splat_file.write(rot[i].astype(np.uint8).tobytes())
            
    
if __name__ == "__main__":
    convert_ply_to_splat(ply_file_to_convert, output_filename)