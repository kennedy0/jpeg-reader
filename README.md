# jpeg reader
![python3.8](https://img.shields.io/badge/python-3.8-blue.svg)

Pure python jpeg reader.

Developed with Python 3.8, but should be compatible with Python 3.6+.

### What this module is
This will get resolution, pixel aspect ratio, and some metadata from most JPEG files.
Additionally, byte offsets to known segment markers are stored.

### What this module isn't
While JPEG files conform to a standard, there are a vast number of application-specific formats for image metadata and thumbnails.
Therefore, this module won't read all metadata from each and every type of JPEG.
That's a rabbit hole I don't care to go down.

### Usage
jpeg_reader can be imported and used as a module to extract information from a JPEG file.

```python
from jpeg_reader import JpegFile


# Get file info from 'test_image.jpg'
jf = JpegFile("test_image.jpg")

# Print file info
print(jf.resolution)
print(jf.pixel_aspect)
for key, value in jf.metadata.items():
    print(key, value)
```

jpeg_reader.py can also be used from the command line to print information about a file

`jpeg_reader.py test_image.jpg`

... or from a folder of jpeg files.

`jpeg_reader.py C:\path\to\images`

## Handy links:

These are links that I found useful for reference.

JPEG: 
* Specs: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
* https://en.wikipedia.org/wiki/JPEG#Syntax_and_structure

APP Segments:
* http://www.ozhiker.com/electronics/pjmt/jpeg_info/app_segments.html

JFIF:
* Specs: http://www.ecma-international.org/publications/files/ECMA-TR/ECMA%20TR-098.pdf
* http://vip.sugovica.hu/Sardi/kepnezo/JPEG%20File%20Layout%20and%20Format.htm
* https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format#File_format_structure

EXIF:
* Specs: https://www.exif.org/Exif2-2.PDF
* https://www.media.mit.edu/pia/Research/deepview/exif.html
