'''入口 获取支持的组合网站  每个网站一个线程  进行初始化线程  每个线程调用 循环获取的任务'''



from spider.ThreadRun import main as mainSpider
#加载log
import log

mainSpider()