import os
import newsml_nitf
import shutil

DIR_NAME = os.path.expanduser("~/Documents/efe/")
DIR_OUT = os.path.expanduser("~/Documents/efe_out/")

with os.scandir(DIR_NAME) as efe_files:
    for file in efe_files:
        if file.name.endswith('.xml'):
            out = open(DIR_OUT + file.name, "w")
            out.write('<?xml version="1.0">')
            out.write('<!DOCTYPE nitf PUBLIC "-//IPTC-NAA//DTD NITF 3.1//EN"')
            out.write('"http://www.nitf.org/site/nitf-documentation/nitf-3-1.dtd"')
            out.close()
            story = newsml_nitf.transformXML(file.path)
            out_binary = open(DIR_OUT + file.name, "wb")
            out_binary.write(story)
            out_binary.close()
        else:
            src = file.path
            dst = DIR_OUT + file.name
            shutil.copy2(src, dst)

