from bs4 import BeautifulSoup
import re
import csv
import time
import requests


class SearchClassify(object):
    def __init__(self, csv_file):
        self.companyinfo = {}
        self.count = 0
        self.company_name = ""
        self.company_name_full = ""
        self.api = 'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles={company_name}&rvprop=content&rvparse'
        self.html_text = ""
        self.classify = ""
        self.category = ""
        self.csv_file = csv_file
        self.menu_file = DEFAULT_MENU_PATH

    def input_company(self, company_name_full):
        self.company_name_full = company_name_full
        self.company_name = self.company_name_full.replace("株式会社", "")
        self.company_name = self.company_name.replace("合同会社", "")
        url = self.api.format(company_name=self.company_name)
        self.find_classify(url)
        self.find_category()
        self.companyinfo.update({
            "name{}".format(str(self.count)): self.company_name_full,
            "classify{}".format(str(self.count)): self.classify,
            "category{}".format(str(self.count)): self.category
        })
        self.count += 1
        return self.companyinfo

    def find_classify(self, url):
        time.sleep(3)
        try:
            request = requests.get(url)
            json_content = request.json()
            j = json_content["query"]["pages"]
            for k in j:
                company_id = k
            self.html_text = j[company_id]["revisions"][0]["*"]
        except:
            self.classify = ""
            self.category = ""
            return self.classify, self.category
        if self.html_text:
            try:
                soup = BeautifulSoup(self.html_text, "lxml")
                candidates = soup.find_all("a")
                a_tag_gyousyu = soup.find("a", title=re.compile("業種"))
                tag_classify = candidates[candidates.index(a_tag_gyousyu) + 1]
                self.classify = self.tag_to_classify(tag_classify)
            except:
                pass
        elif self.html_text.find("th", text=re.compile("団体種類")):
            try:
                str_page_all = self.html_text
                dantai_split1 = str_page_all.split('団体種類</th>')
                dantai_split2 = dantai_split1[1].split('td class="" itemprop="" style="">')
                dantai_split3 = dantai_split2[1].split('</td>')
                tag_classify = dantai_split3[0]
                self.classify = self.tag_to_classify(tag_classify)
            except:
                pass
        elif "省" in self.company_name or "庁" in self.company_name:
            self.classify = "官公庁"
        elif "大学" in self.company_name or "学園" in self.company_name:
            self.classify = "文教"
        elif "市" in self.company_name \
                or "区" in self.company_name \
                or "町" in self.company_name \
                or "村" in self.company_name:
            self.classify = "市区町村"
        else:
            self.category = ""
            self.classify = ""
        return self.classify, self.category

    def tag_to_classify(self, tag_classify):
        item_str = str(tag_classify)
        classify_split1 = item_str.split('">')
        classify_split2 = classify_split1[1].split("</a>")
        classify = classify_split2[0]
        return classify

    def find_category(self):
        with open(self.menu_file, 'r+') as f:
            reader = csv.reader(f)
            templist = []
            tempcount = 0
            for r in reader:
                templist[tempcount*2:tempcount*2] = r
                tempcount += 1
            try:
                i = templist.index(self.classify) + 1
                self.category = templist[i]
            except:
                pass
        return self.category
