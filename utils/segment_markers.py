# Start of Frame markers, non-differential, Huffman coding
SOF0 = 0xffc0  # Baseline DCT
SOF1 = 0xffc1  # Extended sequential DCT
SOF2 = 0xffc2  # Progressive DCT
SOF3 = 0xffc3  # Lossless (sequential)

# Start of Frame markers, differential, Huffman coding
SOF5 = 0xffc5  # Differential sequential DCT
SOF6 = 0xffc6  # Differential progressive DCT
SOF7 = 0xffc7  # Differential lossless (sequential)

# Start of Frame markers, non-differential, arithmetic coding
JPG = 0xffc8  # Reserved for JPEG extensions
SOF9 = 0xffc9  # Extended sequential DCT
SOF10 = 0xffca  # Progressive DCT
SOF11 = 0xffcb  # Lossless (sequential)

# Start of Frame markers, differential, arithmetic coding
SOF13 = 0xffcd  # Lossless (sequential)
SOF14 = 0xffce  # Lossless (sequential)
SOF15 = 0xffcf  # Lossless (sequential)

SOF_MARKERS = (SOF0, SOF1, SOF3, SOF5, SOF6, SOF7, SOF9, SOF10, SOF11, SOF13, SOF14, SOF15)


# Huffman table specification
DHT = 0xffc4  # Define Huffman Table(s)

# Arithmetic coding conditioning specification
DAC = 0xffcc  # Define arithmetic coding conditioning(s)

# Restart interval termination
RST0 = 0xffd0  # Restart with modulo 8 count 0
RST1 = 0xffd1  # Restart with modulo 8 count 1
RST2 = 0xffd2  # Restart with modulo 8 count 2
RST3 = 0xffd3  # Restart with modulo 8 count 3
RST4 = 0xffd4  # Restart with modulo 8 count 4
RST5 = 0xffd5  # Restart with modulo 8 count 5
RST6 = 0xffd6  # Restart with modulo 8 count 6
RST7 = 0xffd7  # Restart with modulo 8 count 7

# Other Markers
SOI = 0xffd8  # Start of image
EOI = 0xffd9  # End of image
SOS = 0xffda  # Start of scan
DQT = 0xffdb  # Define quantization table(s)
DNL = 0xffdc  # Define number of lines
DRI = 0xffdd  # Define restart interval
DHP = 0xffde  # Define hierarchical progression
EXP = 0xffdf  # Expand reference component(s)

# Reserved for application segments
APP0 = 0xffe0  # JFIF
APP1 = 0xffe1  # EXIF
APP2 = 0xffe2  # EXIF
APP3 = 0xffe3
APP4 = 0xffe4
APP5 = 0xffe5
APP6 = 0xffe6
APP7 = 0xffe7
APP8 = 0xffe8
APP9 = 0xffe9
APPA = 0xffea
APPB = 0xffeb
APPC = 0xffec
APPD = 0xffed
APPE = 0xffee
APPF = 0xffef

# Reserved for JPEG extensions
JPG0 = 0xfff0
JPG1 = 0xfff1
JPG2 = 0xfff2
JPG3 = 0xfff3
JPG4 = 0xfff4
JPG5 = 0xfff5
JPG6 = 0xfff6
JPG7 = 0xfff7
JPG8 = 0xfff8
JPG9 = 0xfff9
JPGA = 0xfffa
JPGB = 0xfffb
JPGC = 0xfffc
JPGD = 0xfffd
JPGE = 0xfffe
JPGF = 0xffff

# Comment
COM = 0xfffe

# Reserved Markers
TEM = 0xff01  # For temporary private use in arithmetic coding
