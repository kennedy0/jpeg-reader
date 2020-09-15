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
                    self._read_jfif_segment(f)
                if ord(b) == self.APP1:
                    self._read_exif_segment(f)
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

    def _read_jfif_segment(self, file):
        """ Get the pixel aspect ratio from a JFIF APP0 segment. """
        # Todo: Add more metadata
        with ReadSegment(file):
            file.seek(7, os.SEEK_CUR)
            version_major, version_minor = struct.unpack('>2B', file.read(2))
            jfif_version = f"{version_major}.{version_minor}"
            density_units = struct.unpack('>B', file.read(1))
            x_density, y_density = struct.unpack('>2H', file.read(4))

            self._metadata.update({
                'JFIFVersion': jfif_version,
                'DensityUnits': density_units,
                'Xdensity': x_density,
                'Ydensity': y_density
            })
            self._pixel_aspect = float(x_density) / float(y_density)

    def _read_exif_segment(self, file):
        """ Get the pixel aspect ratio from an EXIF APP1 segment. """
        tag_names = {
            0x0100: "ImageWidth",
            0x0101: "ImageLength",
            0x0102: "BitsPerSample",
            0x0103: "Compression",
            0x0106: "PhotometricInterpretation",
            0x0112: "Orientation",
            0x0115: "SamplesPerPixel",
            0x011c: "PlanarConfiguration",
            0x0212: "YCbCrSubSampling",
            0x0213: "YCbCrPositioning",
            0x011a: "XResolution",
            0x011b: "YResolution",
            0x0128: "ResolutionUnit",
            0x0111: "StripOffsets",
            0x0116: "RowsPerStrip",
            0x0117: "StripByteCounts",
            0x0201: "JPEGInterchangeFormat",
            0x0202: "JPEGInterchangeFormatLength",
            0x012d: "TransferFunction",
            0x013e: "WhitePoint",
            0x013f: "PrimaryChromaticities",
            0x0211: "YCbCrCoefficients",
            0x0214: "ReferenceBlackWhite",
            0x0132: "DateTime",
            0x010e: "ImageDescription",
            0x010f: "Make",
            0x0110: "Model",
            0x0131: "Software",
            0x013b: "Artist",
            0x8298: "Copyright",
        }

        tag_types = {
            1: 'B',  # BYTE
            2: 's',  # ASCII
            3: 'H',  # SHORT
            4: 'L',  # LONG
            5: '2L',  # RATIONAL (Two LONGs; first is the numerator, second is the denominator)
            7: 'B',  # UNDEFINED (8-bit byte that can take any value)
            9: 'l',  # SLONG
            10: '2l',  # SRATIONAL (Two SLONGs; first is the numerator, second is the denominator)
        }

        def _get_byte_count(tag_type, count):
            """ Return the number of bytes for a given tag. """
            if tag_type in ['B', 's']:
                tag_bytes = 1
            elif tag_type in ['H']:
                tag_bytes = 2
            elif tag_type in ['L', 'l']:
                tag_bytes = 4
            elif tag_type in ['2L', '2l']:
                tag_bytes = 8
            else:
                raise RuntimeError(f"Unsupported tag type: {tag_type}")
            return tag_bytes * count

        with ReadSegment(file):
            file.seek(8, os.SEEK_CUR)
            tiff_header_offset = file.tell()

            # Get byte order
            byte_order_signature = struct.unpack('>2s', file.read(2))[0]
            byte_order_signature = byte_order_signature.decode('utf-8')
            if byte_order_signature == "II":
                # 0x4949, Intel, little-endian
                endian = '<'
            elif byte_order_signature == "MM":
                # 0x4d4d, Motorola, big-endian
                endian = '>'
            else:
                pos = hex(file.tell())
                print(f"Unsupported byte order signature at {pos}: {byte_order_signature}")
                return

            # Validate byte order; next 2 bytes are always 0x002a (42)
            bytes_42 = struct.unpack(f'{endian}H', file.read(2))[0]
            assert bytes_42 == 0x002a, "EXIF data order does not match byte order signature."

            # Next 4 bytes is the offset to the IFD0, from the TIFF header.
            ifd_offset = struct.unpack(f'{endian}I', file.read(4))[0]
            file.seek(tiff_header_offset + ifd_offset, os.SEEK_SET)

            # Iterate over each interoperability. See Exif2-2.PDF pg. 102 for more info.
            interop_count = struct.unpack(f'{endian}H', file.read(2))[0]
            for x in range(interop_count):
                tag_id = struct.unpack(f'{endian}H', file.read(2))[0]
                type_id = struct.unpack(f'{endian}H', file.read(2))[0]
                count = struct.unpack(f'{endian}L', file.read(4))[0]

                if tag_id == 0x8769:
                    # EXIF IFD Pointer
                    # Todo: figure out what to do with this. Skip for now.
                    file.seek(4)
                    continue

                tag_name = tag_names.get(tag_id)
                tag_type = tag_types.get(type_id)
                total_bytes = _get_byte_count(tag_type, count)
                if tag_type == 's':
                    tag_type = f'{count}s'

                if total_bytes <= 4:
                    # When total bytes is 4 or less, next 4 bytes stores the value.
                    value = struct.unpack(f'{endian}{tag_type}', file.read(total_bytes))
                    file.seek(4-total_bytes, os.SEEK_CUR)  # Handle padding
                else:
                    # When total bytes is greater than 4, the next 4 bytes stores the offset to the value.
                    value_offset = struct.unpack(f'{endian}I', file.read(4))[0]
                    current_offset = file.tell()
                    file.seek(tiff_header_offset+value_offset, os.SEEK_SET)
                    value = struct.unpack(f'{endian}{tag_type}', file.read(total_bytes))
                    file.seek(current_offset, os.SEEK_SET)

                if len(value) == 1:
                    value = value[0]
                elif len(value) == 2:
                    # Rational numbers
                    value = value[0] / value[1]

                if tag_type.endswith('s'):
                    value = value[:-1]  # Remove null byte
                    value = value.decode('utf-8')

                self._metadata.update({tag_name: value})

            x_resolution = self.metadata.get('XResolution')
            y_resolution = self.metadata.get('YResolution')
            if x_resolution is not None and y_resolution is not None and y_resolution != 0:
                self._pixel_aspect = float(x_resolution) / float(y_resolution)


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
    import pprint
    pprint.pprint(photoshop.metadata)

    print("\n=== img_photoshop_2par ===")
    photoshop_2 = JpegFile("img_photoshop_2par.jpg")
    print("resolution", photoshop_2.resolution, photoshop_2.pixel_aspect)
    pprint.pprint(photoshop_2.metadata)

