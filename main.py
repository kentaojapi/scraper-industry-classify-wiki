from classify_apps.controll import controllcsv
import json
import urllib3
import requests


def main():
    operator = controllcsv.ControllCsv()
    operator.read_csv()
    operator.write_csv(operator.logic.companyinfo)


if __name__ == '__main__':
    main()
