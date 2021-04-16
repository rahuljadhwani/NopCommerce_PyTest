import pytest
from selenium import webdriver
from pageObjects.LoginPage import LoginPage
from utilities import readProperties
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import XLUtil
import time


class Test_0002_login_DDT:
    baseUrl = ReadConfig.getAppUrl()
    path = ".\\TestData\\LoginData.xlsx"
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_login(self, setup):
        self.logger.info("********* Login_002 DDT test starts *********")
        self.logger.info("************** Verifying Login test DDT *************")
        self.driver = setup
        self.driver.get(self.baseUrl)
        self.lp = LoginPage(self.driver)
        list_status=[]

        self.rows = XLUtil.getRowCount(self.path, 'Sheet1')
        print(" total number of rows", self.rows)

        for r in range(2, self.rows+1):
            self.username = XLUtil.readData(self.path, 'Sheet1', r, 1)
            self.password = XLUtil.readData(self.path, 'Sheet1', r, 2)
            self.exp  = XLUtil.readData(self.path, 'Sheet1', r, 3)

            self.lp.setUserName(self.username)
            self.lp.setPassword(self.password)
            self.lp.clickLogin()
            time.sleep(5)

            act_title = self.driver.title
            exp_title =  "Dashboard / nopCommerce administration"

            if act_title==exp_title:
                if self.exp=="Pass":
                    self.logger.info("****** Test Step Passed******")
                    self.lp.clickLogout()
                    list_status.append("Pass")
                elif self.exp=="Fail":
                    self.logger.info("****** Test Step Failed******")
                    # self.lp.clickLogout()
                    list_status.append("Fail")

            elif act_title!=exp_title:
                if self.exp=="Pass":
                    self.logger.info("****** Test Step Failed ******")
                    # self.lp.clickLogout()
                    list_status.append("Fail")
                elif self.exp=="Fail":
                    self.logger.info("****** Test Step Passed ******")
                    # self.lp.clickLogout()
                    list_status.append("Pass")

        # print(list_status)
        if "Fail" not in list_status:
            self.logger.info("******* Login DDT test passed ******")
            self.driver.close()
            assert True
        else:
            self.logger.info("******* Login DDT test failed ******")
            self.driver.close()
            assert False

        self.logger.info("********* End of Login_002 DDT test *********")
