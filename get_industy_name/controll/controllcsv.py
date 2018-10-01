import csv
from classify_apps.controll import scraping


DEFAULT_CSV_PATH = '../csv/company'


class ControllCsv(object):
    def __init__(self):
        self.csv_file = DEFAULT_CSV_PATH
        self.logic = scraping.SearchClassify(self.csv_file)
        self.company_count = 0

    def read_csv(self):
        with open(self.csv_file, 'r+', encoding='utf-8') as f:
            reader = csv.reader(f)
            for c in reader:
                company_name_full = c[0]
                self.logic.input_company(company_name_full)
                self.company_count += 1

    def write_csv(self, dict):
        with open(self.csv_file, 'w+') as f:
            writer = csv.writer(f)
            for x in range(self.company_count):
                templist = [
                    dict["name{}".format(x)],
                    dict["classify{}".format(x)],
                    dict["category{}".format(x)]
                ]
                writer.writerow(templist)
