# 不开启浏览器得到返回值
    # -*- coding:utf-8 -*-
from selenium import webdriver
import time
 
 
# 加载启动项，这里设置headless，表示不启动浏览器，只开一个监听接口获取返回值
option = webdriver.ChromeOptions()
option.add_argument('headless')
 
# 通过url访问浏览器
driver = webdriver.Chrome(chrome_options=option)
url = 'https://www.baidu.com'
 
driver.get(url=url)
 
# 这个是打印page，有的全部打下来
print(driver.page_source)
time.sleep(2)
 
# 退出并关闭浏览器
driver.quit()