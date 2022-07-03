#!/usr/local/bin/python3

from time import sleep
import logging

from selenium import webdriver
import numpy as np


def initWebdriver():
    logging.info('Iniciando el crondriver \n')
    return webdriver.Chrome(r'/Users/joseluis/Downloads/chromedriver')


def openUrl(driver, url):
    driver.get(url)


def acceptCookies(driver):
    try:
        driver.find_element_by_id("truste-consent-button").click()
    except:
        print("")
    sleep(2)


def changeToCelsius(driver):
    driver.find_element_by_id("wuSettings").click()
    sleep(5)
    driver.find_element_by_xpath("//a[@title='Switch to Metric']").click()
    sleep(2)


def getTableInfo(driver):
    sleep(3)
    return driver.find_element_by_class_name("days")


def clear_list(list):
    i = 0
    while (i < len(list)):
        if i > 0 and (float(list[i][3]) < 2 or float(list[i][4]) < 2 or float(list[i][5]) < 2 or float(list[i][6]) < 2):
            del list[i]
        else:
            i = i + 1


def operateTable(table, lista, anio, mes):
    listlist = []
    tbody = table.find_element_by_tag_name("tbody").find_element_by_tag_name("tr")
    td = tbody.find_elements_by_xpath('./*')
    td.pop(6)
    i = 0
    for col in td:
        table = col.find_element_by_tag_name("table")
        colcol = table.find_elements_by_xpath('./*')
        num_element = len(colcol)
        for x in range(num_element):
            if x > 0:
                if i < 1:
                    listlist.append([anio, mes, colcol[x].text])
                else:
                    if i > 0:
                        listlist[x - 1].append(colcol[x].find_elements_by_tag_name("td")[1].text)
        i = i + 1

    for i in listlist:
        lista.append(i)
    return lista


def run(driver, list_atr, year, month):
    sleep(5)
    acceptCookies(driver)
    changeToCelsius(driver)
    table = getTableInfo(driver)
    return operateTable(table, list_atr, year, month)


def main():
    driver = initWebdriver()
    years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    list_atr = [["Year", "Month", "Day", "Temperature", "Dew Point", "Humidity", "Wind Speed", "Pressure"]]
    for year in years:
        for month in months:
            openUrl(driver, "https://www.wunderground.com/history/monthly/es/badajoz/LEBZ/date/"
                    + year + "-" + month)
            list = run(driver, list_atr, year, month)
    driver.close()
    clear_list(list)
    np.savetxt("prueba.csv", list, delimiter=",", fmt="% s")


main()
