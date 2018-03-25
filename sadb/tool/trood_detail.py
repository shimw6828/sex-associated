from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# obj = webdriver.PhantomJS("/opt/phantomjs/bin/phantomjs")



def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    path = "/opt/shimw/chrome/chromedriver"
    obj = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)

    obj.maximize_window()
    obj.set_window_size(1980, 1080)
    obj.get('http://asia.ensembl.org/info/about/speciestree.html')
    obj.find_element_by_id('switch').click()
    obj.find_element_by_class_name("close").click()

    f_nodes = open("/opt/shimw/github/sex-associated/sadb/static/file/nodes.txt", 'w')
    f_nodes.write("ID\tScientific Name\tEnsembl Name\tTaxon ID\tDivergence Time(million Years)\n")
    f_roots = open("/opt/shimw/github/sex-associated/sadb/static/file/roots.txt", 'w')
    f_roots.write("ID\tScientific Name\tEnsembl Name\tTaxon ID\tAssembly\tSpecies Homepage\n")
    for node in obj.find_elements_by_css_selector("[class='inner tnt_tree_node']"):
        node.click()
        id = node.get_attribute("id")
        Scientific_Name = obj.find_element_by_class_name('tnt_zmenu_header').find_element_by_tag_name("th").text
        Scientific_Name=Scientific_Name[17:]
        tds = obj.find_elements_by_class_name("tnt_zmenu_row")
        temp = [id,Scientific_Name]
        for td in tds:
            temp.append(td.find_element_by_tag_name("td").text)
        str="\t".join(temp)+"\n"
        obj.find_element_by_class_name("tnt_tooltip_closer").click()
        f_nodes.write(str)


    for node in obj.find_elements_by_css_selector("[class='leaf tnt_tree_node']"):
        node.find_element_by_tag_name("text").click()
        id = node.get_attribute("id")
        Scientific_Name = obj.find_element_by_class_name('tnt_zmenu_header').find_element_by_tag_name("th").text
        Scientific_Name=Scientific_Name[17:]
        tds = obj.find_elements_by_class_name("tnt_zmenu_row")
        temp = [id,Scientific_Name]
        for td in tds:
            temp.append(td.find_element_by_tag_name("td").text)
        str="\t".join(temp)+"\n"
        obj.find_element_by_class_name("tnt_tooltip_closer").click()
        f_roots.write(str)

    f_nodes.close()
    f_roots.close()


if __name__ == "__main__":
    main()



