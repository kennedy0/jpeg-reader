import os
import struct


def read_jpeg(fp):
    print(f"reading {os.path.abspath(fp)}")
    with open(fp, 'rb') as f:
        soi = struct.unpack('>H', f.read(2))[0]  # Start of image
        assert soi == 0xffd8, "File is not a JPEG file!"
        print(f"soi: {format(soi, 'x')}")

        app_marker = struct.unpack('>H', f.read(2))[0]
        if app_marker not in [0xffe0, 0xffe1]:
            raise IOError(f"Unknown app marker: {format(app_marker, 'x')}")
        print(f"app marker: {format(app_marker, 'x')}")

        marker_length = struct.unpack('>H', f.read(2))[0]
        print(f"app marker length: {marker_length}")

        identifier = struct.unpack('>4s', f.read(4))[0]
        identifier = identifier.decode('utf-8')
        f.seek(1, os.SEEK_CUR)

        version_major, version_minor = struct.unpack('>2B', f.read(2))

        print(f"format version: {identifier} {version_major}.{version_minor}")




if __name__ == "__main__":
    read_jpeg("img_paint.jpg")  # JFIF
    # read_jpeg("img_photoshop.jpg")  # EXIF
