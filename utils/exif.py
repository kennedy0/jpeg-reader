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


def get_byte_count(tag_type, count):
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