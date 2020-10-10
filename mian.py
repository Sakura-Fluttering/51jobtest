import urllib.parse
import urllib.request
import re
from bs4 import BeautifulSoup
import time

class Job51(object):
    def __init__(self, key, page,sleep):
        self.key = key
        self.page = page
        self.sleep = sleep
    
    def listurl(self):
        key = urllib.parse.quote(urllib.parse.quote(self.key))
        ls = []
        for page in range(1, self.page + 1):
            url = "https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html".format(key, page)
            page += 1
            head = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68"
            }
            f = urllib.request.Request(url, headers=head)
            print('开始采集第%d页'%(page-1))
            htmlb = urllib.request.urlopen(f)
            html = htmlb.read().decode('gbk')
            print(html)
            data1 = BeautifulSoup(html, 'html.parser')
            aa_b = re.findall('window.__SEARCH_RESULT__ = (.*?)</script', str(data1))
            aa = re.findall(
                '"job_href":"(.*?)".*?"job_name":"(.*?)".*?"company_href":"(.*?)".*?"providesalary_text":"(.*?)".*?"workarea":"(.*?)".*?"workarea_text":"(.*?)"',
                str(aa_b))
            if bool(aa) == False:
                print("采集结束,目标站搜索结果只有%d页" % (page - 2))
                break
            else:
                for item in aa:
                    s1 = item[0].replace(r"\\", "")  # 招聘详情链接
                    s2 = item[1].replace(r"\\", "")  # 招聘标题
                    # s3 = item[2].replace(r"\\", "")  # 招聘详情
                    s4 = item[3].replace(r"\\", "")  # 工资情况
                    # s5 = item[4].replace(r"\\", "")  #
                    s6 = item[5].replace(r"\\", "")  # 所属地区
                    a = [s1, s2, s4, s6]
                    ls.append(a)
                print('第 %d 页采集入库完成,等待%s秒'%(page - 1,self.sleep))
                time.sleep(self.sleep)
        print("共采集%d条数据" % (len(ls)))
        return ls


def main():
    key = input('输入搜索关键词:')
    page = int(input('采集前多少页:'))
    stime = int(input("每页完成后等待几秒:"))
    cjdata = Job51(key, page,stime)
    data = cjdata.listurl()
    print('创建文件"51job搜索结果采集数据.txt"')
    f = open("51job搜索结果采集数据.txt", "w+", encoding='utf-8')
    f.write(str(data))
    f.close()
    print('成功保存"51job搜索结果采集数据.txt"')
    


if __name__ == '__main__':
    main()