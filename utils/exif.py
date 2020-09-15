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
    0x829a: 'ExposureTime',
    0x829d: 'FNumber',
    0x8822: 'ExposureProgram',
    0x8824: 'SpectralSensitivity',
    0x8827: 'ISOSpeedRatings',
    0x8828: 'OECF',
    0x9000: 'ExifVersion',
    0x9003: 'DateTimeOriginal',
    0x9004: 'DateTimeDigitized',
    0x9101: 'ComponentsConfiguration',
    0x9102: 'CompressedBitsPerPixel',
    0x9201: 'ShutterSpeedValue',
    0x9202: 'ApertureValue',
    0x9203: 'BrightnessValue',
    0x9204: 'ExposureBiasValue',
    0x9205: 'MaxApertureValue',
    0x9206: 'SubjectDistance',
    0x9207: 'MeteringMode',
    0x9208: 'LightSource',
    0x9209: 'Flash',
    0x920a: 'FocalLength',
    0x9214: 'SubjectArea',
    0x927c: 'MakerNote',
    0x9286: 'UserComment',
    0x9290: 'SubSecTime',
    0x9291: 'SubSecTimeOriginal',
    0x9292: 'SubSecTimeDigitized',
    0xa000: 'FlashpixVersion',
    0xa001: 'ColorSpace',
    0xa002: 'PixelXDimension',
    0xa003: 'PixelYDimension',
    0xa004: 'RelatedSoundFile',
    0xa005: 'Pointer',
    0xa20b: 'FlashEnergy',
    0xa20c: 'SpatialFrequencyResponse',
    0xa20e: 'FocalPlaneXResolution',
    0xa20f: 'FocalPlaneYResolution',
    0xa210: 'FocalPlaneResolutionUnit',
    0xa214: 'SubjectLocation',
    0xa215: 'ExposureIndex',
    0xa217: 'SensingMethod',
    0xa300: 'FileSource',
    0xa301: 'SceneType',
    0xa302: 'CFAPattern',
    0xa401: 'CustomRendered',
    0xa402: 'ExposureMode',
    0xa403: 'WhiteBalance',
    0xa404: 'DigitalZoomRatio',
    0xa405: 'FocalLengthIn35mmFilm',
    0xa406: 'SceneCaptureType',
    0xa407: 'GainControl',
    0xa408: 'Contrast',
    0xa409: 'Saturation',
    0xa40a: 'Sharpness',
    0xa40b: 'DeviceSettingDescription',
    0xa40c: 'SubjectDistanceRange',
    0xa420: 'ImageUniqueID',
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
