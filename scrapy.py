from selenium import webdriver

# 创建 Chrome 浏览器实例
driver = webdriver.Chrome()

# 加载百度搜索结果页面
driver.get('https://www.baidu.com/s?wd=selenium')

# 获取所有搜索结果的标题和链接
results = driver.find_elements_by_xpath('//div[@class="result c-container "]')

for result in results:
    # 获取结果标题
    title_element = result.find_element_by_xpath('.//h3/a')
    title = title_element.text

    # 获取结果链接
    link_element = result.find_element_by_xpath('.//h3/a')
    link = link_element.get_attribute('href')

    # 打印结果标题和链接
    print(title)
    print(link)

# 关闭浏览器实例
driver.quit()
