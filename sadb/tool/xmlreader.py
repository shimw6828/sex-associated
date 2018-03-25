try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import argparse,os
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

def getxml(filename):


    tree = ET.parse(filename)
    root=tree.getroot()
    basename=filename.split("/")[-1]
    csvfile = open("/home/zhangna/SAdatabase/result/Biosample/V3.0/" + basename.split(".")[0] + ".csv", "w")
    csvfile.write("SRA,taxonomy_name,taxonomy_id,sex,tissue,age,accession\n")
    for biosample in root:
        try:
            SRA=biosample.find("Ids").find(".//Id[@db='SRA']").text
        except:
            SRA=""
        taxonomy_name=biosample.find("Description").find("Organism").attrib["taxonomy_name"]
        taxonomy_id=biosample.find("Description").find("Organism").attrib["taxonomy_id"]
        try:
            sex=biosample.find("Attributes").find(".//Attribute[@display_name='sex']").text
        except:
            sex=""
        try:
            tissue=biosample.find("Attributes").find(".//Attribute[@display_name='tissue']").text
        except:
            tissue=""
        try:
            age=biosample.find("Attributes").find(".//Attribute[@display_name='age']").text
        except:
            age=""
        try:
            accession=biosample.attrib["accession"]
        except:
            accession=""
        sep=","
        csvfile.write(SRA+sep+taxonomy_name+sep+taxonomy_id+sep+sex+sep+tissue+sep+age+sep+accession+"\n")

    csvfile.close()










if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='xml file')
    args = parser.parse_args()
    filename = args.filename
    getxml(filename)