class SegmentMarker:
    def __init__(self, marker, code, description):
        self.marker = marker
        self.code = code
        self.description = description

    def __str__(self):
        return f"{self.code} ({self.description})"


# Start of Frame markers, non-differential, Huffman coding
SOF0 = SegmentMarker(0xffc0, 'SOF0', 'Baseline DCT')
SOF1 = SegmentMarker(0xffc1, 'SOF1', 'Extended sequential DCT')
SOF2 = SegmentMarker(0xffc2, 'SOF2', 'Progressive DCT')
SOF3 = SegmentMarker(0xffc3, 'SOF3', 'Lossless (sequential)')

# Start of Frame markers, differential, Huffman coding
SOF5 = SegmentMarker(0xffc5, 'SOF5', 'Differential sequential DCT')
SOF6 = SegmentMarker(0xffc6, 'SOF6', 'Differential progressive DCT')
SOF7 = SegmentMarker(0xffc7, 'SOF7', 'Differential lossless (sequential)')

# Start of Frame markers, non-differential, arithmetic coding
JPG = SegmentMarker(0xffc8, 'JPG', 'Reserved for JPEG extensions')
SOF9 = SegmentMarker(0xffc9, 'SOF9', 'Extended sequential DCT')
SOF10 = SegmentMarker(0xffca, 'SOF10', 'Progressive DCT')
SOF11 = SegmentMarker(0xffcb, 'SOF11', 'Lossless (sequential)')

# Start of Frame markers, differential, arithmetic coding
SOF13 = SegmentMarker(0xffcd, 'SOF13', 'Lossless (sequential)')
SOF14 = SegmentMarker(0xffce, 'SOF14', 'Lossless (sequential)')
SOF15 = SegmentMarker(0xffcf, 'SOF15', 'Lossless (sequential)')

SOF_MARKERS = (SOF0, SOF1, SOF3, SOF5, SOF6, SOF7, SOF9, SOF10, SOF11, SOF13, SOF14, SOF15)


# Huffman table specification
DHT = SegmentMarker(0xffc4, 'DHT', 'Define Huffman Table(s)')

# Arithmetic coding conditioning specification
DAC = SegmentMarker(0xffcc, 'DAC', 'Define arithmetic coding conditioning(s)')

# Restart interval termination
RST0 = SegmentMarker(0xffd0, 'RST0', 'Restart with modulo 8 count 0')
RST1 = SegmentMarker(0xffd1, 'RST1', 'Restart with modulo 8 count 1')
RST2 = SegmentMarker(0xffd2, 'RST2', 'Restart with modulo 8 count 2')
RST3 = SegmentMarker(0xffd3, 'RST3', 'Restart with modulo 8 count 3')
RST4 = SegmentMarker(0xffd4, 'RST4', 'Restart with modulo 8 count 4')
RST5 = SegmentMarker(0xffd5, 'RST5', 'Restart with modulo 8 count 5')
RST6 = SegmentMarker(0xffd6, 'RST6', 'Restart with modulo 8 count 6')
RST7 = SegmentMarker(0xffd7, 'RST7', 'Restart with modulo 8 count 7')

RST_MARKERS = (RST0, RST1, RST2, RST3, RST4, RST5, RST6, RST7)

# Other Markers
SOI = SegmentMarker(0xffd8, 'SOI', 'Start of image')
EOI = SegmentMarker(0xffd9, 'EOI', 'End of image')
SOS = SegmentMarker(0xffda, 'SOS', 'Start of scan')
DQT = SegmentMarker(0xffdb, 'DQT', 'Define quantization table(s)')
DNL = SegmentMarker(0xffdc, 'DNL', 'Define number of lines')
DRI = SegmentMarker(0xffdd, 'DRI', 'Define restart interval')
DHP = SegmentMarker(0xffde, 'DHP', 'Define hierarchical progression')
EXP = SegmentMarker(0xffdf, 'EXP', 'Expand reference component(s)')

OTHER_MARKERS = (SOI, EOI, SOS, DQT, DNL, DRI, DHP, EXP)

# Reserved for application segments
APP0 = SegmentMarker(0xffe0, 'APP0', 'JFIF Application Segment')
APP1 = SegmentMarker(0xffe1, 'APP1', 'EXIF, XMP Application Segment')
APP2 = SegmentMarker(0xffe2, 'APP2', 'EXIF, ICC Application Segment')
APP3 = SegmentMarker(0xffe3, 'APP3', 'Application Segment')
APP4 = SegmentMarker(0xffe4, 'APP4', 'Application Segment')
APP5 = SegmentMarker(0xffe5, 'APP5', 'Application Segment')
APP6 = SegmentMarker(0xffe6, 'APP6', 'Application Segment')
APP7 = SegmentMarker(0xffe7, 'APP7', 'Application Segment')
APP8 = SegmentMarker(0xffe8, 'APP8', 'Application Segment')
APP9 = SegmentMarker(0xffe9, 'APP9', 'Application Segment')
APPA = SegmentMarker(0xffea, 'APPA', 'Application Segment')
APPB = SegmentMarker(0xffeb, 'APPB', 'Application Segment')
APPC = SegmentMarker(0xffec, 'APPC', 'Application Segment')
APPD = SegmentMarker(0xffed, 'APPD', 'Application Segment')
APPE = SegmentMarker(0xffee, 'APPE', 'Application Segment')
APPF = SegmentMarker(0xffef, 'APPF', 'Application Segment')

APP_MARKERS = (APP0, APP1, APP2, APP3, APP4, APP5, APP6, APP7, APP8, APP9, APPA, APPB, APPC, APPD, APPE, APPF)


# Reserved for JPEG extensions
JPG0 = SegmentMarker(0xfff0, 'JPG0', 'Reserved for JPEG extensions')
JPG1 = SegmentMarker(0xfff1, 'JPG1', 'Reserved for JPEG extensions')
JPG2 = SegmentMarker(0xfff2, 'JPG2', 'Reserved for JPEG extensions')
JPG3 = SegmentMarker(0xfff3, 'JPG3', 'Reserved for JPEG extensions')
JPG4 = SegmentMarker(0xfff4, 'JPG4', 'Reserved for JPEG extensions')
JPG5 = SegmentMarker(0xfff5, 'JPG5', 'Reserved for JPEG extensions')
JPG6 = SegmentMarker(0xfff6, 'JPG6', 'Reserved for JPEG extensions')
JPG7 = SegmentMarker(0xfff7, 'JPG7', 'Reserved for JPEG extensions')
JPG8 = SegmentMarker(0xfff8, 'JPG8', 'Reserved for JPEG extensions')
JPG9 = SegmentMarker(0xfff9, 'JPG9', 'Reserved for JPEG extensions')
JPGA = SegmentMarker(0xfffa, 'JPGA', 'Reserved for JPEG extensions')
JPGB = SegmentMarker(0xfffb, 'JPGB', 'Reserved for JPEG extensions')
JPGC = SegmentMarker(0xfffc, 'JPGC', 'Reserved for JPEG extensions')
JPGD = SegmentMarker(0xfffd, 'JPGD', 'Reserved for JPEG extensions')
JPGE = SegmentMarker(0xfffe, 'JPGE', 'Reserved for JPEG extensions')
JPGF = SegmentMarker(0xffff, 'JPGF', 'Reserved for JPEG extensions')

JPG_MARKERS = (JPG0, JPG1, JPG2, JPG3, JPG4, JPG5, JPG6, JPG7, JPG8, JPG9, JPGA, JPGB, JPGC, JPGD, JPGE, JPGF)

# Comment
COM = SegmentMarker(0xfffe, 'COM', 'Comment')

# Reserved Markers
TEM = SegmentMarker(0xff01, 'TEM', 'For temporary private use in arithmetic coding')

SEGMENT_MARKERS = SOF_MARKERS + (DHT, DAC) + RST_MARKERS + OTHER_MARKERS + APP_MARKERS + JPG_MARKERS + (COM, TEM)


def get_segment_marker(marker):
    """ Get a SegmentMarker tuple from marker bytes. """
    for segment in SEGMENT_MARKERS:
        if segment.marker == marker:
            return segment
    return None
