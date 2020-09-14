import os
import struct
from typing import BinaryIO


class ReadSegment:
    """ Context manager for reading a JPEG segment. Upon finishing, it moves the current position offset to the end of
    the segment.

    JPEG files store metadata in segments, which always contain the following 4 bytes:
    ff MM LLLL
    Where,
        ff = Segment marker identifier
        MM = Segment marker type
        LLLL = Segment length, not including first 2 bytes of identifier and type
    """
    def __init__(self, file: BinaryIO):
        self.file = file
        self.segment_end = None

    def __enter__(self):
        segment_length = struct.unpack('>H', self.file.read(2))[0]
        self.segment_end = self.file.tell() + segment_length - 2
        self.file.seek(-2, os.SEEK_CUR)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.seek(self.segment_end, os.SEEK_SET)


class JpegFile:
    # Segment Markers
    SOI = 0xd8  # Start of Image
    SOF0 = 0xc0  # Start of Frame (baseline DCT)
    SOF2 = 0xc2  # Start of Frame (progressive DCT)
    DHT = 0xc4  # Define Huffman Table(s)
    DQT = 0xdb  # Define Quantization Table(s)
    DRI = 0xdd  # Define Restart Interval
    SOS = 0xda  # Start of Scan
    APP0 = 0xe0  # JFIF APP0
    APP1 = 0xe1  # EXIF APP1
    COM = 0xfe  # Comment
    EOI = 0xd9  # End of Image

    def __init__(self, file_path):
        self._file_path = file_path
        self._resolution = (None, None)
        self._pixel_aspect = None
        self._metadata = dict()  # Any extra non-standard information

        self._read_file()

    @property
    def resolution(self):
        return self._resolution

    @property
    def pixel_aspect(self):
        return self._pixel_aspect

    @property
    def metadata(self):
        return self._metadata

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
                    self._get_resolution_baseline(f)
                if ord(b) == self.SOF2:
                    self._get_resolution_progressive(f)
                if ord(b) == self.DHT:
                    self._skip_segment(f)
                if ord(b) == self.DQT:
                    self._skip_segment(f)
                if ord(b) == self.DRI:
                    self._skip_segment(f)
                if ord(b) == self.SOS:
                    self._skip_segment(f)
                if ord(b) == self.APP0:
                    self._get_pixel_aspect_jfif(f)
                if ord(b) == self.APP1:
                    self._get_pixel_aspect_exif(f)
                if ord(b) == self.COM:
                    self._skip_segment(f)

                b = f.read(1)

    @staticmethod
    def _skip_segment(file):
        """ Skip an unimplemented segment. """
        with ReadSegment(file):
            pass

    def _get_resolution_baseline(self, file):
        """ Get the resolution from a SOF (baseline DCT) segment """
        with ReadSegment(file):
            file.seek(3, os.SEEK_CUR)
            width, height = struct.unpack('>2H', file.read(4))
            self._resolution = (width, height)

    def _get_resolution_progressive(self, file):
        """ Get the resolution from a SOF (progressive DCT) segment """
        raise NotImplementedError("Progressive DCT images not supported.")

    def _get_pixel_aspect_jfif(self, file):
        """ Get the pixel aspect ratio from a JFIF APP0 segment. """
        with ReadSegment(file):
            file.seek(10, os.SEEK_CUR)
            x_density, y_density = struct.unpack('>2H', file.read(4))
            self._pixel_aspect = float(x_density) / float(y_density)

    def _get_pixel_aspect_exif(self, file):
        """ Get the pixel aspect ratio from an EXIF APP1 segment. """
        tag_names = {
            0x0100: "ImageWidth",
            0x0101: "ImageLength",
            0x0102: "BitsPerSample",
        }

        tag_types = {
            1: 'B',  # BYTE
            2: 'c',  # ASCII
            3: 'H',  # SHORT
            4: 'L',  # LONG
            5: '2L',  # RATIONAL (Two LONGs; first is the numerator, second is the denominator)
            7: 'B',  # UNDEFINED (8-bit byte that can take any value)
            9: 'l',  # SLONG
            10: '2l',  # SRATIONAL (Two SLONGs; first is the numerator, second is the denominator)
        }

        with ReadSegment(file):
            # Get byte order
            file.seek(8, os.SEEK_CUR)
            byte_order_signature = struct.unpack('>2s', file.read(2))[0]
            byte_order_signature = byte_order_signature.decode('utf-8')
            if byte_order_signature == "II":
                # 0x4949, Intel, little-endian
                endian = '<'
            elif byte_order_signature == "MM":
                # 0x4d4d, Motorola, big-endian
                endian = '>'
            else:
                print(f"Unsupported byte order signature: {byte_order_signature}")
                return

            # Validate byte order; next 2 bytes are always 0x002a (42)
            bytes_42 = struct.unpack(f'{endian}H', file.read(2))[0]
            assert bytes_42 == 0x002a, "EXIF data order does not match byte order signature."

            # Next 4 bytes is the offset to the IFD0 (main Image File Directory; value includes TIFF header.
            ifd_offset = struct.unpack(f'{endian}I', file.read(4))[0]
            ifd_offset -= 8  # Compensate for TIFF header length
            file.seek(ifd_offset, os.SEEK_CUR)

            # Iterate over each interoperability. See Exif2-2.PDF pg. 102 for more info.
            interop_count = struct.unpack(f'{endian}H', file.read(2))[0]
            for x in range(interop_count):
                tag_id = struct.unpack(f'{endian}H', file.read(2))[0]
                data_type = struct.unpack(f'{endian}H', file.read(2))[0]
                count = struct.unpack(f'{endian}B', file.read(2))[0]

if __name__ == "__main__":
    print("\n=== img_paint ===")
    paint = JpegFile("img_paint.jpg")
    print("resolution", paint.resolution, paint.pixel_aspect)

    print("\n=== img_natron ===")
    natron = JpegFile("img_natron.jpg")
    print("resolution", natron.resolution, natron.pixel_aspect)

    print("\n=== img_photoshop ===")
    photoshop = JpegFile("img_photoshop.jpg")
    print("resolution", photoshop.resolution, photoshop.pixel_aspect)

    print("\n=== img_photoshop_2par ===")
    photoshop_2 = JpegFile("img_photoshop_2par.jpg")
    print("resolution", photoshop_2.resolution, photoshop_2.pixel_aspect)

