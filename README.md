[toc]

一、Appium简介
--

##### 什么是Appium

Appium是一个开源测试自动化框架，可用于原生，混合和移动Web应用程序测试。 它使用WebDriver协议驱动iOS，Android和Windows应用程序。

##### Appium的优势
- 可以跨平台同时支持Android、iOS
- 支持多种语言，java、python、php、Ruby等等

二、环境配置
--

1、 安装homebrew：

```sh
#通过`brew -v` 查看是否安装成功
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

```

2、安装node && npm：

下载pkg直接安装：http://nodejs.cn/download/

```
#v12.11.1
node -v
#6.11.3
npm -v
```

3、iOS环境安装

```sh

#安装libimobiledevice
brew install libimobiledevice --HEAD

#安装carthage：
brew install carthage

#安装ios-deploy：
npm install -g ios-deploy

#安装xcode && XCT（xcode命令行工具）

```

8、安装appium-doctor

```sh
#中间可能会提示更新npm或者权限
sudo npm install -g appium-doctor

#检测环境配置
appium-doctor --ios

```

![](https://raw.githubusercontent.com/vhbvb/image_cloud/master/general20200103174532.png)

9、安装appium

官方下载地址：https://github.com/appium/appium-desktop/releases


<br/>

三、配置appium 
--

Appium-mac-1.15.0-1版本

##### 1. 配置webdriver

```sh
cd /Applications/Appium.app/Contents/Resources/app/node_modules/appium/node_modules/appium-webdriveragent 

#加载工程依赖库
sh Scripts/bootstrap.sh

#打开工程目录，用xcode打开WebDriverAgent.xcodeproj
open WebDriverAgent.xcodeproj
```

配置xcode开发者账号或者证书，配置编译成功后直接关掉即可

![](https://raw.githubusercontent.com/vhbvb/image_cloud/master/general20200103174602.png)

![](https://raw.githubusercontent.com/vhbvb/image_cloud/master/general20200103174625.png)

##### 2. appium 客户端配置

1、打开appium, 直接点击启动服务，Port默认为4723

![](https://raw.githubusercontent.com/vhbvb/image_cloud/master/general20200103174635.png)

2、新建Session

![](https://raw.githubusercontent.com/vhbvb/image_cloud/master/general20200103174647.png)

![](https://raw.githubusercontent.com/vhbvb/image_cloud/master/general20200103174701.png)

字段说明：

```
{
  "platformName": "iOS", #平台类型
  "deviceName": "iPhone 8 Plus", #机型
  "automationName": "XCUITest",#写死XCUITest
  "platformVersion": "13.1.2",#系统版本号
  "udid": "9619555fae75f4957abba4f52fa26ac3d47fb758",#测试真机的udid
  "bundleId": "com.mob.product.ShareSDK"# 测试机上安装的测试demo包名
}
```

3、 启动 Session

- 测试机确认安装了测试包，并且已信任证书可以正常打开
- 点击 Start Session

![](https://raw.githubusercontent.com/vhbvb/image_cloud/master/general20200103174725.png)

<br/>

四、Python 环境编写UI单元测试用例
--

##### 安装Appium-Python-Client

```sh
#sudo pip install Appium-Python-Client
sudo pip3 install Appium-Python-Client
```

##### pycharm示例项目代码：


```python
import unittest
import time
from appium import webdriver

class ShareSDKUnitTest(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '13.1.2'
        desired_caps['deviceName'] = 'iPhone 8 Plus'
        desired_caps['automationName'] = "XCUITest"
        desired_caps["udid"] = "9619555fae75f4957abba4f52fa26ac3d47fb758"
        desired_caps["bundleId"] = "com.mob.product.ShareSDK"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def share_unit(self,unit,process):
        self.click_if_enabled(unit)
        time.sleep(3)
        process()
        time.sleep(3)
        self.click_if_enabled("确定")

    # 分享菜单测试
    def test_menu(self):
        self.click_if_enabled("shareMenuIcon")
        self.click_if_enabled("取消")

    # 抖音平台测试
    def test_share_douyin(self):
        self.click_if_enabled("抖音")

        def process_1():
            self.click_if_enabled("返回")
        def process_2():
            self.click_if_enabled("icon segment bigback")
        def process_3():
            self.click_if_enabled("icon segment bigback")
            self.click_if_enabled("确认")

        self.share_unit("图片",process_1)
        self.share_unit("相册图片",process_1)
        self.share_unit("单个视频",process_2)
        self.share_unit("多个视频",process_3)

    # QQ平台测试
    def test_share_qq(self):

        self.click_if_enabled("QQ")
        def process(): self.click_if_enabled("取消")

        self.share_unit("文字", process)
        self.share_unit("图片", process)
        self.share_unit("链接", process)
        self.share_unit("音乐链接", process)
        self.share_unit("视频链接", process)

        def mini_process(): self.click_if_enabled("返回美的厨房")
        self.share_unit("小程序", mini_process)

    # 新浪菜单测试
    def test_menu_sina(self):
        self.click_if_enabled("shareMenuIcon")
        self.click_if_enabled("新浪微博")
        self.click_if_enabled("转发到微博")
        self.click_if_enabled("确定")

    def test_share_wechat(self):
        self.click_if_enabled("微信好友")
        def process(): self.click_if_enabled("关闭")

        self.share_unit("文字", process)
        self.share_unit("图片", process)
        self.share_unit("链接", process)
        self.share_unit("音乐链接", process)
        self.share_unit("视频链接", process)
        self.share_unit("应用消息", process)
        self.share_unit("表情", process)
        self.share_unit("文件（本地视频）", process)
        self.share_unit("小程序", process)

    def click_if_enabled(self,el):
        elem_name = "name =='{}'".format(el)
        for i in range(0,10):
            try:
                el = self.driver.find_element_by_ios_predicate(elem_name)
                el.click()
                break
            except Exception as e:
                # print("\n Exception:{},timeout:{}".format(e,i))
                if i == 9:
                    raise SyntaxError("elem:{} click()".format(elem_name)) from e
            time.sleep(1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ShareSDKUnitTest)
    unittest.TextTestRunner(verbosity=2).run(suite)(verbosity=2).run(suite)
```


#### 注意事项

1. ==避免使用 xpath 查询 element，速度极慢==

    控件查询速度顺序：
    
    ```
    ios_predicate >> accessibility_id >> class_name >>xpath
    ```

    参考：https://www.cnblogs.com/xiaoxi-3-/p/9620881.html


2. 如果执行单元测试过程中出现： 

    appium ConnectionResetError: [Errno 54] Connection reset by peer
    
    time.sleep 时间不要太长 不要超过5s