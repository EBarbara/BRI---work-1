from lxml import etree


def load_config(config_file):
    global input_files, list_file
    input_files = []
    with open(config_file) as config:
        for line in config:
            operation = line.rstrip().split('=')[0]
            file = line.rstrip().split('=')[1]
            if operation == 'LEIA':
                input_files.append(file)
            elif operation == 'ESCREVA':
                list_file = file


def read_data(input_file):
    parser = etree.XMLParser(dtd_validation=True)
    file = etree.parse(input_file, parser)

    for record in file.getroot().iterchildren():
        for element in record.iterchildren():
            if element.tag == 'RECORDNUM':
                print(element.tag, element.text)
            elif element.tag == 'ABSTRACT':
                print(element.tag, element.text)
            elif element.tag == 'EXTRACT':
                print(element.tag, element.text)
        print("-------------------------------")
    return file


load_config('config/gli.cfg')
for input_file in input_files:
    read_data(input_file)
