# Scrape NBA injuries news and send the recapitulative table by mail
import os
from selenium import webdriver
import pandas as pd
from datetime import date

global driver

from Send_mail import *

driver = webdriver.Chrome(executable_path = "C:\\Users\\Utilisateur\\Desktop\\scrapeOP-master\\chromedriver_win32\\chromedriver.exe")
driver.get('https://www.rotoworld.com/basketball/nba/injury-report')

########################### I - First define the functions
def ffi(a):
    try:
        return(driver.find_element_by_xpath(a).text)
    except:
        return(None)

def collect_info_line(team, i):
    TEAM = ffi('//*[@id="injury-report-page-wrapper"]/div/div[2]/div[{}]/a/div/div[2]'.format(team))
    player = ffi('//*[@id="injury-report-page-wrapper"]/div/div[2]/div[{}]/div/div/div[1]/table/tbody/tr[{}]/td[1]/span/a'.format(team, i))
    position = ffi('//*[@id="injury-report-page-wrapper"]/div/div[2]/div[{}]/div/div/div[1]/table/tbody/tr[{}]/td[2]'.format(team, i))
    status = ffi('//*[@id="injury-report-page-wrapper"]/div/div[2]/div[{}]/div/div/div[1]/table/tbody/tr[{}]/td[3]'.format(team, i))
    date = ffi('//*[@id="injury-report-page-wrapper"]/div/div[2]/div[{}]/div/div/div[1]/table/tbody/tr[{}]/td[4]'.format(team, i))
    injury = ffi('//*[@id="injury-report-page-wrapper"]/div/div[2]/div[{}]/div/div/div[1]/table/tbody/tr[{}]/td[5]'.format(team, i))
    returns = ffi('//*[@id="injury-report-page-wrapper"]/div/div[2]/div[{}]/div/div/div[1]/table/tbody/tr[{}]/td[6]'.format(team, i))

    if player is not None:
        print(TEAM, player, status)
    return([TEAM, player, position, status, date, injury, returns])

########################## II - Now scrape the page...
Injuries = []
for team in range(1, 31):
    for i in range(1, 50):
        info = collect_info_line(team, i)
        if info[1] is not None:
            Injuries.append(info)
        else: # if we have info[1] is None it means that there is no more injuries for this team : we go to next team
            break

########################## III - Save the csv and send by mail
Injuries = pd.DataFrame(Injuries)
Injuries.columns = ['Team', 'Player', 'Position', 'Status', 'News date', 'Injury', 'Return date']
Injuries.to_csv('Injuries_report_{}.csv'.format(date.today()), index = False, sep = ';')

send_mail_csv(file_path = 'Injuries_report_{}.csv'.format(date.today()))
driver.quit()


