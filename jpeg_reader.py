import os
import pprint
import struct
import sys
import traceback
from typing import BinaryIO

from utils import constants
from utils import exif
from utils import segment_markers


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
    def __init__(self, file_path):
        self._file_path = file_path
        self._resolution = (None, None)
        self._pixel_aspect = None
        self._metadata = dict()

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
            soi = self._find_next_marker(f)
            assert soi == segment_markers.SOI, f"File is not a JPEG file: {self._file_path}"

            while True:
                marker = self._find_next_marker(f)
                if marker == segment_markers.EOI:
                    # Stop reading file if we are at End of Image
                    return

                # Get resolution from any SOF marker.
                if marker in segment_markers.SOF_MARKERS:
                    self._get_resolution(f)
                    continue
                elif marker in segment_markers.APP_MARKERS:
                    self._read_app_segment(f)
                    continue
                else:
                    self._skip_segment(f)

    @staticmethod
    def _find_next_marker(file):
        """ Find and return the next marker (2 bytes). """
        # Find first byte following 0xff that is not 0xff or null
        b1, b2 = file.read(2)
        while b1 != 0xff:
            file.seek(-1, os.SEEK_CUR)
            b1, b2 = file.read(2)
            while b2 == 0x00 or b2 == 0xff:
                file.seek(-1, os.SEEK_CUR)
                b1, b2 = file.read(2)

        # Read marker
        marker = b1 << 8 | b2
        return marker

    @staticmethod
    def _skip_segment(file):
        """ Skip an unimplemented segment. """
        with ReadSegment(file):
            pass

    def _get_resolution(self, file):
        """ Get the resolution from a SOF frame header segment. """
        with ReadSegment(file):
            file.seek(3, os.SEEK_CUR)
            height, width = struct.unpack('>2H', file.read(4))
            self._resolution = (width, height)

    def _read_app_segment(self, file):
        """ Read an APP segment and handle any known segment types. """
        with ReadSegment(file):
            file.seek(2, os.SEEK_CUR)  # Skip segment length
            if self._unpack_header_string(file, 4) in [constants.JFIF_HEADER, constants.JFXX_HEADER]:
                self._read_jfif_segment(file)
                return
            elif self._unpack_header_string(file, 4) == constants.EXIF_HEADER:
                self._read_exif(file)
                return

    def _read_jfif_segment(self, file):
        """ Read the JFIF APP0 segment. """
        file.seek(5, os.SEEK_CUR)  # Skip JFIF header string

        version_major, version_minor = struct.unpack('>2B', file.read(2))
        jfif_version = f"{version_major}.{version_minor}"
        density_units = struct.unpack('>B', file.read(1))[0]
        x_density, y_density = struct.unpack('>2H', file.read(4))

        self._metadata.update({
            'JFIFVersion': jfif_version,
            'DensityUnits': density_units,
            'Xdensity': x_density,
            'Ydensity': y_density
        })
        self._pixel_aspect = float(x_density) / float(y_density)

    @staticmethod
    def _unpack_header_string(file, length):
        """ Read the next characters as a string. """
        start_pos = file.tell()
        # noinspection PyBroadException
        try:
            header = struct.unpack(f'>{length}s', file.read(length))[0]
            header = header.decode('utf-8')
        except Exception:
            header = None
        finally:
            file.seek(start_pos, os.SEEK_SET)
        return header

    def _read_exif(self, file):
        file.seek(6, os.SEEK_CUR)
        tiff_header_offset = file.tell()

        try:
            endian = self._get_exif_byte_order(file, tiff_header_offset)
        except Exception as e:
            print(e)
            return

        self._read_exif_ifds(file, tiff_header_offset, endian)

        # Update pixel aspect ratio
        x_resolution = self.metadata.get('XResolution')
        y_resolution = self.metadata.get('YResolution')
        if x_resolution is not None and y_resolution is not None and y_resolution != 0:
            self._pixel_aspect = float(x_resolution) / float(y_resolution)

    @staticmethod
    def _get_exif_byte_order(file, tiff_header_offset):
        """ Get byte order for EXIF APP segment. """
        file.seek(tiff_header_offset, os.SEEK_SET)
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
            raise RuntimeError(f"Unsupported byte order signature at {pos}: {byte_order_signature}")

        # Validate byte order; next 2 bytes are always 0x002a (42)
        bytes_42 = struct.unpack(f'{endian}H', file.read(2))[0]
        assert bytes_42 == 0x002a, "EXIF data order does not match byte order signature."

        return endian

    def _read_exif_ifds(self, file, tiff_header_offset, endian):
        """ Read all IFDs from an EXIF Segment and set metadata. """
        # Get offset to the first IFD, from the TIFF header.
        file.seek(tiff_header_offset, os.SEEK_SET)
        file.seek(4, os.SEEK_CUR)
        ifd_pointer = struct.unpack(f'{endian}I', file.read(4))[0]
        ifd0_offset = tiff_header_offset + ifd_pointer

        # Get info from IFD0.
        ifd0_data = self._get_ifd_data(
           file,
           ifd0_offset,
           tiff_header_offset,
           endian,
           tag_names=exif.tiff_tag_names)

        # IDF0 will contain pointer to EXIF IFD.
        # noinspection PyBroadException
        try:
            exif_ifd_tag = exif.tiff_tag_names.get(0x8769)
            exif_ifd_pointer = ifd0_data.pop(exif_ifd_tag)
            exif_ifd_offset = tiff_header_offset + exif_ifd_pointer
            exif_ifd_data = self._get_ifd_data(
                file,
                exif_ifd_offset,
                tiff_header_offset,
                endian,
                tag_names=exif.exif_tag_names)
        except Exception:
            exif_ifd_data = {}

        # IDF0 may contain optional GPSInfo pointer.
        # noinspection PyBroadException
        try:
            gpsinfo_ifd_tag = exif.tiff_tag_names.get(0x8825)
            gpsinfo_ifd_pointer = ifd0_data.pop(gpsinfo_ifd_tag)
            gpsinfo_ifd_offset = tiff_header_offset + gpsinfo_ifd_pointer
            gpsinfo_ifd_data = self._get_ifd_data(
                file,
                gpsinfo_ifd_offset,
                tiff_header_offset,
                endian,
                tag_names=exif.gpsinfo_tag_names)
        except Exception:
            gpsinfo_ifd_data = {}

        self._metadata.update(ifd0_data)
        self._metadata.update(exif_ifd_data)
        self._metadata.update(gpsinfo_ifd_data)

    def _get_ifd_data(self, file, ifd_offset, tiff_header_offset, endian, tag_names):
        """ Iterate over each interoperability. """
        ifd_data = dict()
        file.seek(ifd_offset, os.SEEK_SET)

        interop_count = struct.unpack(f'{endian}H', file.read(2))[0]
        for x in range(interop_count):
            tag_id = struct.unpack(f'{endian}H', file.read(2))[0]
            type_id = struct.unpack(f'{endian}H', file.read(2))[0]
            count = struct.unpack(f'{endian}L', file.read(4))[0]

            tag_name = tag_names.get(tag_id)
            tag_type = exif.tag_types.get(type_id)
            total_bytes = exif.get_byte_count(tag_type, count)
            if tag_type == 's':
                tag_type = f'{count}s'

            if tag_type is None:
                # Skip fields with UNDEFINED types
                # TODO: Get value for UNDEFINED field types
                file.seek(4)
                continue

            elif total_bytes <= 4:
                # When total bytes is 4 or less, next 4 bytes stores the value.
                value = struct.unpack(f'{endian}{tag_type}', file.read(total_bytes))
                file.seek(4 - total_bytes, os.SEEK_CUR)  # Handle padding
            else:
                # When total bytes is greater than 4, the next 4 bytes stores the offset to the value.
                value_offset = struct.unpack(f'{endian}I', file.read(4))[0]
                current_offset = file.tell()
                file.seek(tiff_header_offset + value_offset, os.SEEK_SET)
                value = struct.unpack(f'{endian}{tag_type}', file.read(total_bytes))
                file.seek(current_offset, os.SEEK_SET)

            # Format values for metadata
            if value is None:
                pass
            elif len(value) == 1:
                value = value[0]
            elif len(value) == 2:
                # Rational numbers
                value = value[0] / value[1]
            if tag_type is not None and tag_type.endswith('s'):
                # Strings
                value = value[:-1]  # Remove null byte
                value = value.decode('utf-8')

            ifd_data.update({tag_name: value})

        return ifd_data


def print_file_info(file_path):
    """ Print out information about a jpeg file. """
    print(f"reading {file_path}")
    jpeg_file = JpegFile(file_path)
    resolution = f"{jpeg_file.resolution[0]} x {jpeg_file.resolution[1]}"
    if jpeg_file.pixel_aspect is not None:
        resolution = f"{resolution} ({jpeg_file.pixel_aspect} PAR)"
    print(f"resolution: {resolution}")
    print(f"metadata: {pprint.pformat(jpeg_file.metadata, compact=False)}")
    print("\n")


if __name__ == "__main__":
    p = sys.argv[1]
    if os.path.isfile(p):
        print_file_info(p)
    elif os.path.isdir(p):
        for item in os.listdir(p):
            if item.endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
                fp = os.path.join(p, item)
                # noinspection PyBroadException
                try:
                    print_file_info(fp)
                except Exception:
                    print(traceback.format_exc())
                    print("\n")
