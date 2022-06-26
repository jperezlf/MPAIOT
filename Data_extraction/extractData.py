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


def operateTable(table, lista, anio, mes):
    listlist = []
    tbody = table.find_element_by_tag_name("tbody").find_element_by_tag_name("tr")
    td = tbody.find_elements_by_xpath('./*')
    # td.pop(2)
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
                    # if i > 0 and i != 5:
                    if i > 0:
                        listlist[x - 1].append(colcol[x].find_elements_by_tag_name("td")[1].text)
                    # elif i == 1:
                    #     listlist[x - 1].append(colcol[x].find_elements_by_tag_name("td")[1].text)
        i = i + 1

    for i in listlist:
        lista.append(i)
    return lista


def run(driver, lista, anio, mes):
    sleep(5)
    acceptCookies(driver)
    changeToCelsius(driver)
    table = getTableInfo(driver)
    return operateTable(table, lista, anio, mes)


def clear_list(list):
    i = 0
    while (i < len(list)):
        if list[i][3] < 2 or list[i][4] < 2 or list[i][5] < 2 or list[i][6] < 2:
            del list[i]
        else:
            i = i + 1


def main():
    driver = initWebdriver()
    # anios = ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
    anios = ["2014"]
    meses = ["08"]
    # meses = ["01", "02", "03", "04", "05", "06"]
    lista = [["Year",
              "Month",
              "Day",
              "Temperature",
              "Dew Point",
              "Humidity",
              "Wind Speed",
              "Pressure"]];
    for anio in anios:
        for mes in meses:
            openUrl(driver, "https://www.wunderground.com/history/monthly/es/badajoz/LEBZ/date/" + anio + "-" + mes)
            lista = run(driver, lista, anio, mes)
    driver.close()
    clear_list(lista)
    np.savetxt("prueba.csv", lista, delimiter=",", fmt="% s")


main()
