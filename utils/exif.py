import struct


tiff_tag_names = {
    0x0100: "ImageWidth",
    0x0101: "ImageLength",
    0x0102: "BitsPerSample",
    0x0103: "Compression",
    0x0106: "PhotometricInterpretation",
    0x010e: "ImageDescription",
    0x010f: "Make",
    0x0110: "Model",
    0x0111: "StripOffsets",
    0x0112: "Orientation",
    0x0115: "SamplesPerPixel",
    0x0116: "RowsPerStrip",
    0x0117: "StripByteCounts",
    0x011a: "XResolution",
    0x011b: "YResolution",
    0x011c: "PlanarConfiguration",
    0x0128: "ResolutionUnit",
    0x012d: "TransferFunction",
    0x0131: "Software",
    0x0132: "DateTime",
    0x013b: "Artist",
    0x013e: "WhitePoint",
    0x013f: "PrimaryChromaticities",
    0x0201: "JPEGInterchangeFormat",
    0x0202: "JPEGInterchangeFormatLength",
    0x0211: "YCbCrCoefficients",
    0x0212: "YCbCrSubSampling",
    0x0213: "YCbCrPositioning",
    0x0214: "ReferenceBlackWhite",
    0x8298: "Copyright",
    0x8769: "Exif IFD Pointer",
    0x8825: "GPSInfo IFD Pointer",
}

exif_tag_names = {
    0x829a: "ExposureTime",
    0x829d: "FNumber",
    0x8822: "ExposureProgram",
    0x8824: "SpectralSensitivity",
    0x8827: "ISOSpeedRatings",
    0x8828: "OECF",
    0x9000: "ExifVersion",
    0x9003: "DateTimeOriginal",
    0x9004: "DateTimeDigitized",
    0x9101: "ComponentsConfiguration",
    0x9102: "CompressedBitsPerPixel",
    0x9201: "ShutterSpeedValue",
    0x9202: "ApertureValue",
    0x9203: "BrightnessValue",
    0x9204: "ExposureBiasValue",
    0x9205: "MaxApertureValue",
    0x9206: "SubjectDistance",
    0x9207: "MeteringMode",
    0x9208: "LightSource",
    0x9209: "Flash",
    0x920a: "FocalLength",
    0x9214: "SubjectArea",
    0x927c: "MakerNote",
    0x9286: "UserComment",
    0x9290: "SubSecTime",
    0x9291: "SubSecTimeOriginal",
    0x9292: "SubSecTimeDigitized",
    0xa000: "FlashpixVersion",
    0xa001: "ColorSpace",
    0xa002: "PixelXDimension",
    0xa003: "PixelYDimension",
    0xa004: "RelatedSoundFile",
    0xa005: "Pointer",
    0xa20b: "FlashEnergy",
    0xa20c: "SpatialFrequencyResponse",
    0xa20e: "FocalPlaneXResolution",
    0xa20f: "FocalPlaneYResolution",
    0xa210: "FocalPlaneResolutionUnit",
    0xa214: "SubjectLocation",
    0xa215: "ExposureIndex",
    0xa217: "SensingMethod",
    0xa300: "FileSource",
    0xa301: "SceneType",
    0xa302: "CFAPattern",
    0xa401: "CustomRendered",
    0xa402: "ExposureMode",
    0xa403: "WhiteBalance",
    0xa404: "DigitalZoomRatio",
    0xa405: "FocalLengthIn35mmFilm",
    0xa406: "SceneCaptureType",
    0xa407: "GainControl",
    0xa408: "Contrast",
    0xa409: "Saturation",
    0xa40a: "Sharpness",
    0xa40b: "DeviceSettingDescription",
    0xa40c: "SubjectDistanceRange",
    0xa420: "ImageUniqueID",
}

gpsinfo_tag_names = {
    0x00: "GPSVersionID",
    0x01: "GPSLatitudeRef",
    0x02: "GPSLatitude",
    0x03: "GPSLongitudeRef",
    0x04: "GPSLongitude",
    0x05: "GPSAltitudeRef",
    0x06: "GPSAltitude",
    0x07: "GPSTimeStamp",
    0x08: "GPSSatellites",
    0x09: "GPSStatus",
    0x0a: "GPSMeasureMode",
    0x0b: "GPSDOP",
    0x0c: "GPSSpeedRef",
    0x0d: "GPSSpeed",
    0x0e: "GPSTrackRef",
    0x0f: "GPSTrack",
    0x10: "GPSImgDirectionRef",
    0x11: "GPSImgDirection",
    0x12: "GPSMapDatum",
    0x13: "GPSDestLatitudeRef",
    0x14: "GPSDestLatitude",
    0x15: "GPSDestLongitudeRef",
    0x16: "GPSDestLongitude",
    0x17: "GPSDestBearingRef",
    0x18: "GPSDestBearing",
    0x19: "GPSDestDistanceRef",
    0x1a: "GPSDestDistance",
    0x1b: "GPSProcessingMethod",
    0x1c: "GPSAreaInformation",
    0x1d: "GPSDateStamp",
    0x1e: "GPSDifferential",
}

tag_types = {
    1: "B",  # BYTE
    2: "s",  # ASCII
    3: "H",  # SHORT
    4: "L",  # LONG
    5: "2L",  # RATIONAL (Two LONGs; first is the numerator, second is the denominator)
    7: None,  # UNDEFINED (8-bit byte that can take any value. Implementation is specific to the field.)
    9: "l",  # SLONG
    10: "2l",  # SRATIONAL (Two SLONGs; first is the numerator, second is the denominator)
}


def get_byte_count(tag_type, count):
    """ Return the number of bytes for a given tag. """
    if tag_type in ['B', 's', None]:
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


def unpack_standard_ifd_value(string: bytes, endian, tag_type):
    """ Unpacks a value from an ifd string, as long as its value is not UNDEFINED. """
    value = struct.unpack(f'{endian}{tag_type}', string)

    # Format values for metadata
    if value is None:
        pass
    elif len(value) == 1:
        value = value[0]
    elif len(value) == 2:
        # Rational numbers
        value = value[0] / value[1]
    if tag_type.endswith('s'):
        # Strings
        null = struct.pack('B', 0x00)
        value = value.strip(null)  # Remove null byte
        value = value.decode('utf-8').strip()

    return value


def unpack_undefined_ifd_value(tag_id, string, count):
    """ Each UNDEFINED ifd type has its own unique data structure.
    See Exif 2.2 specs starting on p.17 for a complete list of UNDEFINED data types and how to read them.
    ToDo: This can be greatly expanded upon should the need arise.
    """
    unpack_fn_dispatch_table = {
        0x9000: unpack_exif_version,  # ExifVersion
        0xa000: unpack_flashpix_version,  # FlashpixVersion
        0x9101: unpack_components_configuration,  # ComponentsConfiguration
        0x927c: unpack_maker_note,  # MakerNote
    }

    def _unpack_unknown(_string, _count):
        return None

    unpack_fn = unpack_fn_dispatch_table.get(tag_id, _unpack_unknown)
    value = unpack_fn(string, count)
    return value


def unpack_exif_version(string, count):
    value = struct.unpack(f'>{count}s', string)[0]
    value = value.decode('utf-8')
    return value


def unpack_flashpix_version(string, count):
    value = struct.unpack(f'>{count}s', string)[0]
    value = value.decode('utf-8')
    return value


def unpack_components_configuration(string, count):
    value = struct.unpack(f'>{count}B', string)
    if value == (4, 5, 6, 0):
        value = "RGB"
    elif value == (1, 2, 3, 0):
        value = "YCbCr"
    return value


def unpack_maker_note(string, count):
    value = struct.unpack(f'>{count}s', string)[0]
    value = value.decode('utf-8')
    return value


