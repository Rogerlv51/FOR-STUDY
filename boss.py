# 导入包，此代码已失效
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import xlwt
import re
# 1.action chains 2.句柄 3.遮挡
# 打开浏览器
driver = webdriver.Chrome()
# 浏览器最大化
driver.maximize_window()
# 打开一个网页
driver.get("https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88&city=101280600")
#让它充分加载
driver.implicitly_wait(10)
driver.execute_script('document.documentElement.scrollTop = document.documentElement.scrollHeight')
#定位元素（标签）css\xpath
# divs = driver.find_elements(By.CSS_SELECTOR, '.itm')
datalists =[]
for page in range(2):
    # current_window = driver.current_window_handle
    # print("current_window:: ", current_window)
    uls = driver.find_elements(By.CSS_SELECTOR,'.job-list ul li')
    # print(uls)
    for ul in uls:

        windows = driver.window_handles
        driver.switch_to.window(windows[0])

        datalist = []

        job_name = ul.find_element(By.CSS_SELECTOR,'.job-name').text
        job_area = ul.find_element(By.CSS_SELECTOR,'.job-area').text
        job_salary = ul.find_element(By.CSS_SELECTOR,'.job-limit .red').text
        job_info = ul.find_element(By.CSS_SELECTOR,'.job-limit p').text
        company_name = ul.find_element(By.CSS_SELECTOR,'.company-text .name a').text
        welfare = ul.find_element(By.CSS_SELECTOR,'.info-append .info-desc').text

        datalist.append(job_name)
        datalist.append(job_area)
        datalist.append(job_salary)
        datalist.append(job_info)
        datalist.append(company_name)
        datalist.append(welfare)
        # 获取标签中的属性
        # href = "https://www.zhipin.com/"+ ul.find_element(By.CSS_SELECTOR, '.primary-box').get_attribute('href')
        content = ul.find_element(By.CSS_SELECTOR, '.job-primary')
        driver.execute_script('arguments[0].click()', content)

        windows = driver.window_handles
        driver.switch_to.window(windows[-1])

        # all_window=driver.window_handles
        # print("all_window:: ", all_window)
        # for window in all_window:  # 通过遍历判断要切换的窗口
        #     print("window:: ", window)
        #     if window != current_window:
        #         driver.switch_to.window(window)
        #         current_window = driver.current_window_handle

        job_desc = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div').text
        job_location = driver.find_element(By.CSS_SELECTOR, '.location-address').text

        datalist.append(job_desc)
        datalist.append(job_location)

        driver.close()
        # time.sleep(2)
        # ActionChains(driver).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        # time.sleep(1)
        # print(datalist)
        # break
        # 模拟点击动作，进入下一页
        datalists.append(datalist)
        break
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
    page_next = driver.find_element(By.CSS_SELECTOR, '.next')
    driver.execute_script('arguments[0].click()', page_next)

    # hidden_submenu = driver.find_element(By.CSS_SELECTOR,".show-top")
    # webdriver.ActionChains(driver).move_to_element(page_next).click(hidden_submenu).perform()

    # 防止点击过快，内容加载不出
    time.sleep(1)

driver.close()
driver.quit()

def saveToexcel(savepath,datalists):

    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("boss直聘DA", cell_overwrite_ok=True)
    name_sheet = ("职位名称", "工作地点", "薪资", "基本要求", "公司", "福利待遇",  "岗位描述", "公司地点")
    for i in range(len(name_sheet)):
        worksheet.write(0, i, name_sheet[i])

    for i in range(len(datalists)):
        item = datalists[i]
        # print("正在查第%d条内容" % ((i + 1)))
        for j in range(len(item)):
            worksheet.write(i + 1, j, item[j])

    workbook.save(savepath)

saveToexcel('boss_DA.xls',datalists)
