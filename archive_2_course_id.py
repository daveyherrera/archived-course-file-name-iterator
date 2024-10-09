import os
import platform
import zipfile
import json
from dataclasses import replace

import xmltodict
from importlib.metadata import files

invalid_characters = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', '¿', '/', '$', '!', "'", '"', ':', '@', '+', '`', '|', '=']

def replace_invalid_chars(input_string, replacement=''):
    for char in invalid_characters:
        input_string = input_string.replace(char, replacement)
    return input_string

# what is the os
current_os = platform.platform()
# Files directory
files_directory = "/Users/davey.herrera/Desktop/Devcon_course_archive/folder"
# first, let's get a list of files on the folder.
work_directory = os.listdir(files_directory)
# remove the hidden mac os file, this prob won't work fine on windows machines
if "mac" in current_os:
    work_directory.remove('.DS_Store')

# Let's start by opening one zip file
# Let's loop this up!
for file in work_directory:
    with zipfile.ZipFile(files_directory + "/" + file, 'r') as zip_file:
    # search for imsmanifest.xml file and extract it only
        zip_file.extract('imsmanifest.xml')

    with open('imsmanifest.xml') as manifest:
        # change the manifest from xml to json
        manifest_dict = xmltodict.parse(manifest.read())
        # find the name of the course object > manifest > resources > resource > 0 _bb:title
        course_id = manifest_dict["manifest"]["resources"]["resource"][0]["@bb:title"]
        # clean the course id from invalid characters that may not be accepted by the file system
        course_id_cleaned = replace_invalid_chars(course_id)
        # replace the file name with the course_id
        os.rename(files_directory + "/" + file, files_directory + "/" + course_id_cleaned + ".zip" )
