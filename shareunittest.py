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
    unittest.TextTestRunner(verbosity=2).run(suite)

