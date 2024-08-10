from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from lxml import etree
from tqdm import tqdm
import ddddocr
import datetime
import time
import warnings

import os
import urllib.request
import subprocess
from pathlib import Path

global stu_info  # 全局变量-学生信息
warnings.filterwarnings('ignore')
# 获取当前路径，定义默认下载路径
current_path = Path(__file__).parent


# 下载所需依赖
def download():
    print("程序需要依赖OCR识别技术，请确认本地是否已安装tesseractOCR")
    print("是（Y/y） 否（N/n）")
    if input() == "Y" or input() == "y":
        exit()
    else:
        print("默认下载路径为py文件当前目录，是否需要更改？")
        print("是（Y/y） 否（N/n）")
        if input() == "Y" or input() == "y":
            download_path = input("请输入下载目录：")
            print("正在下载OCR安装包，请稍候------")
            download()
        else:
            download_path = current_path
            print("正在下载OCR安装包，请稍候------")
    # 定义远程安装包的URL
    remote_url = "https://cloud.viper3.top/d/%F0%9F%8D%87%E9%98%BF%E9%87%8C%E4%BA%91%E7%9B%98/%E5%AE%89%E8%A3%85%E5%8C%85/tesseract-ocr-w64-setup-5.3.1.20230401.exe"

    # 定义本地文件的完整路径，将其保存到桌面
    local_filename = download_path / "tesseractOCR-Win64Setup5.3.1.20230401.exe"  # 保存到桌面的文件名

    # 下载安装包
    urllib.request.urlretrieve(remote_url, local_filename)
    print("下载完成")
    print("即将安装OCR包，请手动完成后续安装，程序将在安装完成后继续运行")
    # 运行安装程序
    subprocess.run(["cmd", "/c", str(local_filename)], shell=True)


# 输入账号密码
def login(username, pwd):
    # 设置Edge浏览器参数
    options = webdriver.EdgeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
    options.use_chromium = True
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用GPU加速
    options.add_argument('--no-sandbox')  # 禁用沙盒
    options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
    options.add_argument("disable-cache")  # 禁用缓存
    options.add_argument('log-level=3')  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    options.add_argument('--disable-extensions')  # 禁用扩展

    # 1.打开Edge浏览器
    global stu_info
    driver = webdriver.Edge(options=options)
    # 2.打开网址
    jwzx_url = "https://jwzx.bipt.edu.cn/academic/common/security/affairLogin.jsp"
    driver.get(jwzx_url)

    # 输入账号
    userInput = driver.find_element(By.XPATH, "/html/body/form/div[2]/div/div[3]/input")
    userInput.click()
    userInput.send_keys(username)

    # 输入密码
    pwdInput = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div[4]/input')
    pwdInput.click()
    pwdInput.send_keys(pwd)

    # 输入验证码
    codeInput = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div[5]/input')  # 输入框位置
    loginBtn = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div[7]/input[2]')  # 登录按钮位置
    # 若登录成功
    jwzx_academic_url = "https://jwzx.bipt.edu.cn/academic/index_frame.jsp"
    codeCount = 1  # 用于计算验证码识别次数
    while True:
        imgCode = driver.find_element(By.XPATH, '//*[@id="jcaptcha"]')  # 图片位置
        timestamp = int(time.time())  # 获取当前时间戳，用于命名验证码图片
        codeImg_name = "code{}.png".format(timestamp)  # 验证码图片命名
        imgCode.screenshot(codeImg_name)  # 将验证码保存，保存为code.png
        print("第{}次正在识别验证码，请稍候……".format(codeCount))
        '''以下为识别验证码的代码'''
        ocr = ddddocr.DdddOcr()
        with open(codeImg_name, "rb") as fp:
            image = fp.read()
        catch = ocr.classification(image)  # 验证码返回给catch
        codeInput.send_keys(catch)  # 将识别到的验证码输入到框内
        # 删除本地保存的验证码图片
        time.sleep(1)
        os.remove(codeImg_name)
        codeCount += 1

        # 点击登录
        loginBtn.click()
        time.sleep(2)

        # 验证该元素是否存在
        def isElementExist(element):
            flag = True
            try:
                driver.find_element(By.XPATH, element)
                return flag
            except:
                flag = False
                return flag

        exists = isElementExist('//*[@id="message"]')

        if exists:
            if driver.current_url != jwzx_academic_url:
                codeInput.clear()  # 清空验证码输入框
                continue
        else:
            driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
            driver.switch_to.frame("headerFrame")  # 使用frame的name属性
            stu_info = driver.find_element(By.XPATH, '//*[@id="greeting"]/span').text
            current_time = datetime.datetime.now().strftime("%H:%M")
            print("您好！{}，欢迎登录 {}".format(stu_info, current_time))
            time.sleep(2)
            break
    time.sleep(1)
    driver.refresh()  # 刷新页面，目的将焦点切换回默认frame
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))  # 切换到iframe
    driver.switch_to.frame("menuFrame")  # 使用frame的name属性
    eduAssessBtn = driver.find_element(By.XPATH, '//*[@id="li18"]/a/span')
    eduAssessBtn.click()
    # 切换到mainFrame
    driver.switch_to.parent_frame()  # 切换到父级frame（frameset）
    driver.switch_to.frame("mainFrame")  # 使用frame的name属性
    # 加上判断未评估课程数量容错机制
    courseList_count = int(len(etree.HTML(driver.page_source).xpath('/html/body/center/table[2]/tbody/tr/td[4]/a[1]/text()')))
    for i in tqdm(range(courseList_count), colour='green', desc='教学评价进度'):
        status = etree.HTML(driver.page_source).xpath('/html/body/center/table[2]/tbody/tr[{}]/td[3]/span/text()'.format(i + 2))[0]
        if status == "未评估":
            assessBtn = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[{}]/td[4]/a[1]'.format(i + 2))
            assessBtn.click()
            questionList_count = int(len(etree.HTML(driver.page_source).xpath('/html/body/center/table[2]/tbody/tr/td/form/table[1]/tbody/tr')))
            for j in range(questionList_count - 3):
                agreeBtn = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr/td/form/table[1]/tbody/tr[{}]/td[3]/input[5]'.format(j + 2))
                agreeBtn.click()
                time.sleep(0.1)
            for k in range(questionList_count - 1, questionList_count + 1):
                suggestText = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr/td/form/table[1]/tbody/tr[{}]/td[3]/textarea'.format(k))
                suggestText.click()
                if k == questionList_count - 1:
                    suggestText.send_keys("E")
                    time.sleep(0.1)
                else:
                    suggestText.send_keys("无")
                    time.sleep(0.1)
            submitBtn = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr/td/form/table[2]/tbody/tr/td/input[1]')
            # 点击提交按钮
            submitBtn.click()
            # 切换到弹窗
            alert = Alert(driver)
            # 点击确定按钮
            alert.accept()
            teacher = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[{}]/td[1]/a'.format(i + 2)).text
            course = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[{}]/td[2]'.format(i + 2)).text
            print(f"您参加的{teacher}教师主讲的《{course}》自动评估完成")
        else:
            teacher = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[{}]/td[1]/a'.format(i + 2)).text
            course = driver.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[{}]/td[2]'.format(i + 2)).text
            print(f"您参加的{teacher}教师主讲的《{course}》先前已完成评估！！！")
        time.sleep(2)

    print("{}的课程已全部完成教学评价".format(stu_info))


def main():
    print("============================")
    print("技术支持由Viper3强力驱动")
    print("Copyright©2023.09.26")
    print("博客地址：viper3.top")
    print("云盘地址：cloud.viper3.top")
    print("============================")
    username = input("请输入您的学号：")
    password = input("请输入您的密码：")
    download()
    print("安装完成，即将进行教学评价……")
    login(username, password)


if __name__ == "__main__":
    main()
