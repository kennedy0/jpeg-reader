import os
import struct


class JpegFile:
    SOI = 0xd8  # Start of Image
    SOF0 = 0xc0  # Start of Frame (baseline DCT)
    SOF2 = 0xc2  # Start of Frame (progressive DCT)
    DHT = 0xc4  # Define Huffman Table(s)
    DQT = 0xdb  # Define Quantization Table(s)
    DRI = 0xdd  # Define Restart Interval
    SOS = 0xda  # Start of Scan
    COM = 0xfe  # Comment
    EOI = 0xd9  # End of Image

    def __init__(self, file_path):
        self._file_path = file_path
        self._resolution = (None, None)
        self._par = None

        self._read_file()

    @property
    def resolution(self):
        return self._resolution

    def _read_file(self):
        with open(self._file_path, 'rb') as f:
            soi = struct.unpack('>H', f.read(2))[0]  # Start of image
            assert soi == 0xffd8, f"File is not a JPEG file: {self._file_path}"

            b = f.read(1)
            while b and ord(b) != self.EOI:
                while ord(b) != 0xff:
                    # FF indicates start of a marker
                    b = f.read(1)
                while ord(b) == 0xff:
                    # Skip any consecutive FF bytes (used as fill bytes for padding)
                    b = f.read(1)

                if ord(b) == self.SOF0:
                    f.seek(3, os.SEEK_CUR)
                    width, height = struct.unpack('>2H', f.read(4))
                    self._resolution = (width, height)

                b = f.read(1)


if __name__ == "__main__":
    jfif = JpegFile("img_paint.jpg")
    print(jfif.resolution)

    exif = JpegFile("img_photoshop.jpg")
    print(exif.resolution)
