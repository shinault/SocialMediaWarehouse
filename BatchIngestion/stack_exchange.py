import DataCollector
import shutil
import requests
import xml.etree.ElementTree as ET

# Build list of 7z files
src = "https://archive.org/download/stackexchange/stackexchange_files.xml"
r = requests.get(src)
with open("xml_file", "wb") as f:
    f.write(r.content)

se_7z_files = []

xml_tree = ET.parse("xml_file")
root = xml_tree.getroot() 
file_nodes = root.findall("file")
for file_node in file_nodes:
    name = file_node.attrib['name']
    if name[-3:] == ".7z":
        se_7z_files.append(name)


# Execute the file transfers
se_base_url = "https://archive.org/download/stackexchange/"
s3_folder = "raw/stack_exchange/"
s3_bucket = "saywhat-warehouse"

if __name__ == "__main__":
    for filename in se_7z_files:
        full_url = se_base_url + filename
        folder_name = filename[:-3]
        print("Downloading file: " + filename)
        DataCollector.download(se_base_url + filename, filename)
        print("Decompressing file: " + filename)
        DataCollector.decompress(filename, "7z", folder_name)
        print("Transferring folder to S3: " + folder_name)
        DataCollector.write_folder_to_S3(folder_name, s3_folder, s3_bucket)
        shutil.rmtree(folder_name)
