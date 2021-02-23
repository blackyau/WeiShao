import csv
import requests
from datetime import datetime
import config
import config_out
import json
from random import uniform
from sys import exit
import argparse

parser = argparse.ArgumentParser(description='微哨健康打卡与检查打卡情况')
parser.add_argument('data', metavar='DataFile', default='userinfo.csv', nargs='?', help='用户数据文件的名字')
parser.add_argument('-c', action='store_true', default=False, help='使用该参数的话就只检查是否打卡')
args = parser.parse_args()


def check(stu_code):
    url = 'http://ncp.suse.edu.cn/api/questionnaire/questionnaire/getQuestionNaireList'
    payload = {'sch_code': 'suse', 'stu_code': stu_code, 'authorityid': 0, 'type': 3, 'pagenum': 1, 'pagesize': 1000,
               'stu_range': 999, 'searchkey': ''}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; LIO-AN00 Build/HUAWEILIO-AN00; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36 weishao(6.7.4.72570) wsi18n('
                      'zh)',
        'X-Requested-With': 'com.ruijie.whistle', 'Referer': 'http://ncp.suse.edu.cn/questionnaire/my'}
    try:
        r = requests.get(url, params=payload, headers=headers, timeout=3)
        if r.ok:
            get_list = r.json()['data']
            if len(get_list) > 0:  # 最近 14 天没打卡
                return False
            sing_time = get_list[0]['createtime']  # 获取最近提交问卷的时间
            now_time = datetime.today().strftime('%Y-%m-%d')  # 获取当前时间
            if sing_time == now_time:
                return True
            else:
                return False
        else:
            print('请求失败,错误信息:', r.text)
            return False
    except requests.exceptions.RequestException as err:
        print(stu_code, "请求失败:", err)


def user_info(stu_code, password):
    post_data_raw = json.loads(json.dumps(config.Postdates))  # 不能直接引用
    post_data_raw["name"] = stu_code
    post_data_raw["password"] = password
    headers = {'Referer': 'http://web.weishao.com.cn/login',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.75 Safari/537.36', 'Content-Type': 'application/json'}
    post_data = json.dumps(post_data_raw)  # 这网站必须要先用json.dumps()转换一下，不然验证会失败
    try:
        r = requests.post('http://web.weishao.com.cn/api/login', headers=headers, data=post_data, timeout=10)
        result = r.json()
        if not r.ok:
            print('登录失败详细信息:', r.text, end='')
            return None
        return result
    except requests.exceptions.RequestException as err:
        print(stu_code, "请求失败:", err)


# 学号, 密码
def fuck_weishao(stu_code, password, add=None):
    headers = {
        'Referer': 'http://ncp.suse.edu.cn/questionnaire/addanswer?page_from=onpublic&activityid=82&can_repeat=1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; LIO-AN00 Build/HUAWEILIO-AN00; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36 weishao(6.7.4.72570) wsi18n('
                      'zh)',
        'Content-Type': 'application/json'}
    if stu_code is None or password is None:
        return False
    if stu_code in DATA and add is None:  # 有缓存的数据，同时地址为空（也就是未在校）
        try:
            r = requests.post('http://ncp.suse.edu.cn/api/questionnaire/questionnaire/addMyAnswer', headers=headers,
                              data=json.dumps(DATA[stu_code]), timeout=10)
            if not r.ok:
                print('打卡失败,错误信息如下:', r.text, end='')
                return None
            else:
                return r.json()
        except requests.exceptions.RequestException as err:
            print("请求失败:", err)
    answer_data = json.loads(json.dumps(config.Answer))
    if add is None:  # 如果是在校（地址为空）就去读取在校的配置
        totalArr_data = json.loads(json.dumps(config.TotalArr))
    else:  # 读取未在校的配置
        totalArr_data = json.loads(json.dumps(config_out.TotalArr))
        totalArr_data[1]['content'] = add  # 把地址写入
    userinfo = user_info(stu_code, password)
    if userinfo is None:
        return ''
    answer_data['stu_code'] = userinfo['student_number']
    answer_data['stu_name'] = userinfo['name']
    answer_data['identity'] = userinfo['identity']
    answer_data['path'] = userinfo['path']
    answer_data['gender'] = userinfo['sex']
    # 拼接 organization
    filler_list = ['&0/', '&3/', '&1/', '&0/', '&0']
    name_list = [i['name'] for i in userinfo['orgPath'][1:]]
    org = ''
    for i in range(len(name_list)):
        org += name_list[i] + filler_list[i]
    answer_data['organization'] = org

    # 随机生成体温
    for i in range(6, 9):
        totalArr_data[i]['content'] = round(uniform(36.2, 36.9), 1)

    # 生成 question_data
    answer_data['totalArr'] = totalArr_data
    question_data = []
    for i in totalArr_data:
        if i['answered']:
            question_data.append(i)
    answer_data['question_data'] = question_data
    try:
        r = requests.post('http://ncp.suse.edu.cn/api/questionnaire/questionnaire/addMyAnswer', headers=headers,
                          data=json.dumps(answer_data), timeout=10)
        if not r.ok:
            print('打卡失败,错误信息如下:', r.text, end='')
            return None
        else:
            DATA[stu_code] = answer_data
            return r.json()
    except requests.exceptions.RequestException as err:
        print("请求失败:", err)


if __name__ == '__main__':
    try:
        with open('Data.json', mode='r', encoding='gbk') as Data_FILE:
            filestr = Data_FILE.read()
            if filestr != "":
                DATA = json.loads(filestr)
    except FileNotFoundError:
        DATA = {}  # 解决第一次运行时,如果这个变量没有被初始化,那么前面登录的代码就会出的问题
    try:
        with open(args.data, mode='r', encoding='gbk') as fp:
            reader = csv.reader(fp)
            # 第一个元素做key，后面的做value，value[0]:名字，value[1]:密码，value[2]:地址（如果有地址就是未在校）
            all_user_info = {rows[0]: tuple(rows[1:]) for rows in reader}
    except FileExistsError:
        print("userinfo.csv 数据文件不存在,请手动创建并按格式写入用户数据")
        exit(1)
    for i in all_user_info.keys():
        if check(i):
            print('{0:\u3000<4s}{1:\u3000>3s}'.format(all_user_info[i][0], '已打卡'))
        else:  # 该用户未打卡
            if args.c:  # 只检查是否打卡
                print('{0:\u3000<4s}{1:\u3000>3s}'.format(all_user_info[i][0], '未打卡'))
            else:  # 要进行补卡
                print('{0:\u3000<4s}{1:\u3000<12s}{2:<16s}{3}'
                      .format(all_user_info[i][0], i, all_user_info[i][1], '打卡结果:'), end='')
                if len(all_user_info[i]) == 2:  # 没有填写地址，提交数据按在校处理
                    print(fuck_weishao(i, all_user_info[i][1]))
                else:  # 填写了地址，按未在校处理
                    print(fuck_weishao(i, all_user_info[i][1], all_user_info[i][2]))
    with open('Data.json', mode='w', encoding='gbk') as Data_FILE:
        Data_FILE.write(json.dumps(DATA, indent=2, ensure_ascii=False))
