from flask import Flask,request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random,time,json,re,requests,os

# 实例化路由
app = Flask(__name__)
num = 0
@app.route("/register", methods=["GET", "POST"])
def requests_get():
    if request.method == "GET":  # get请求
        return 'GET请求'
    if request.method == "POST": # post请求
        jsonInfo = request.get_data()  # 获取请求数据  {'url':'http://xxxxxxx'}
        info=jsonInfo.decode()  # urlencode 解码
        info = json.loads(info)  # json 转为 字典
        url=(info['url'])  # 取值
        print(url)
        times = int(time.time()) + random.randint(1, 100)
        name = str(times)
        name = name + '.jpg'  # 生成随机图片名
        Info=page(url,name)  # 进行解析
        return Info
def page(url,name):
    x = requests.get(url)
    with open(name, 'wb') as f:
        for chunk in x.iter_content(chunk_size=32):
            f.write(chunk)
        f.close()
    mobile_emulation = {"deviceName": "Nexus 5"}  # 改为手机模式
    chrome_options = Options()  # 实例化
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)  # 把手机模式的参数添加到Options里
    chrome_options.add_argument("--headless")  # 设置隐藏浏览器
    chrome_options.add_argument('--disable-gpu')  # 设置隐藏浏览器
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 启动浏览器
    driver.implicitly_wait(30)  # 等待
    driver.get("https://www.baidu.com/")  # 访问连接
    driver.find_element_by_id("ts-image-uploader-icon").click()  # 点击事件
    time.sleep(0.5)  # 此处必须等待加载完毕 不然点击不了相机
    driver.find_element_by_xpath(
        u"(.//*[normalize-space(text()) and normalize-space(.)='识别商品'])[1]/following::input[1]").click()
    driver.find_element_by_xpath(
        u"(.//*[normalize-space(text()) and normalize-space(.)='识别商品'])[1]/following::input[1]").clear()
    driver.find_element_by_xpath(
        u"(.//*[normalize-space(text()) and normalize-space(.)='识别商品'])[1]/following::input[1]").send_keys(
        "C:\\Users\\Administrator\\Desktop\\Baidu.com\\%s" % name)  # 上传照片

    time.sleep(3)  # 等待三秒加载页面
    html = driver.page_source  # 获取html
    # driver.close()
    driver.quit()  # 关闭浏览器
    time.sleep(0.5)  # 等待删除
    os.remove("C:\\Users\\Administrator\\Desktop\\Baidu.com\\%s" % name)  # 删除照片
    info_re = re.compile(
        r'</span><span class="graph-imgtext-desc-value graph-c-guess-img-text-desc-value">(.*?)\s+</span></p>')
    info = info_re.findall(html)   # 获取数据
    # if info != []:  # 如果数据正常直接返回
    dictInfo = dict()
    dictInfo['品牌']=info[0]
    dictInfo['类别']=info[1]
    Info = json.dumps(dictInfo)
    return Info
    # global num
    # if info == [] and num < 3:   # 如果抓取不到数据，则循环 三次获取数据
    #     num+=1
    #     page(url, name)
    # if num > 3:   # 如果三次都没有抓到此产品就直接放弃
    #     dictInfo = dict()
    #     dictInfo['品牌'] = '无法识别'
    #     dictInfo['类别'] = '无法识别'
    #     Info = json.dumps(dictInfo)
    #     return Info


if __name__ == "__main__":
    app.run(port=8000, debug=True,)