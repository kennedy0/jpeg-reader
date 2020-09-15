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
    'ExposureTime': 0x829a,
    'FNumber': 0x829d,
    'ExposureProgram': 0x8822,
    'SpectralSensitivity': 0x8824,
    'ISOSpeedRatings': 0x8827,
    'OECF': 0x8828,
    'ExifVersion': 0x9000,
    'DateTimeOriginal': 0x9003,
    'DateTimeDigitized': 0x9004,
    'ComponentsConfiguration': 0x9101,
    'CompressedBitsPerPixel': 0x9102,
    'ShutterSpeedValue': 0x9201,
    'ApertureValue': 0x9202,
    'BrightnessValue': 0x9203,
    'ExposureBiasValue': 0x9204,
    'MaxApertureValue': 0x9205,
    'SubjectDistance': 0x9206,
    'MeteringMode': 0x9207,
    'LightSource': 0x9208,
    'Flash': 0x9209,
    'FocalLength': 0x920a,
    'SubjectArea': 0x9214,
    'MakerNote': 0x927c,
    'UserComment': 0x9286,
    'SubSecTime': 0x9290,
    'SubSecTimeOriginal': 0x9291,
    'SubSecTimeDigitized': 0x9292,
    'FlashpixVersion': 0xa000,
    'ColorSpace': 0xa001,
    'PixelXDimension': 0xa002,
    'PixelYDimension': 0xa003,
    'RelatedSoundFile': 0xa004,
    'Pointer': 0xa005,
    'FlashEnergy': 0xa20b,
    'SpatialFrequencyResponse': 0xa20c,
    'FocalPlaneXResolution': 0xa20e,
    'FocalPlaneYResolution': 0xa20f,
    'FocalPlaneResolutionUnit': 0xa210,
    'SubjectLocation': 0xa214,
    'ExposureIndex': 0xa215,
    'SensingMethod': 0xa217,
    'FileSource': 0xa300,
    'SceneType': 0xa301,
    'CFAPattern': 0xa302,
    'CustomRendered': 0xa401,
    'ExposureMode': 0xa402,
    'WhiteBalance': 0xa403,
    'DigitalZoomRatio': 0xa404,
    'FocalLengthIn35mmFilm': 0xa405,
    'SceneCaptureType': 0xa406,
    'GainControl': 0xa407,
    'Contrast': 0xa408,
    'Saturation': 0xa409,
    'Sharpness': 0xa40a,
    'DeviceSettingDescription': 0xa40b,
    'SubjectDistanceRange': 0xa40c,
    'ImageUniqueID': 0xa420,
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
