import csv
import requests
from datetime import datetime
import config
import json
from random import uniform


def check(stu_code):
    url = 'http://ncp.suse.edu.cn/api/questionnaire/questionnaire/getQuestionNaireList'
    payload = {'sch_code': 'suse', 'stu_code': stu_code, 'authorityid': 0, 'type': 3, 'pagenum': 1, 'pagesize': 1000,
               'stu_range': 999, 'searchkey': ''}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; LIO-AN00 Build/HUAWEILIO-AN00; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36 weishao(6.7.4.72570) wsi18n('
                      'zh)',
        'X-Requested-With': 'com.ruijie.whistle', 'Referer': 'http://ncp.suse.edu.cn/questionnaire/my'}
    r = requests.get(url, params=payload, headers=headers)
    if r.ok:
        sing_time = r.json()['data'][0]['createtime']  # 获取最近提交问卷的时间
        now_time = datetime.today().strftime('%Y-%m-%d')  # 获取当前时间
        if sing_time == now_time:
            return True
        else:
            return False
    else:
        print('请求失败,错误信息:', r.text)
        return False


def user_info(stu_code, password):
    post_data_raw = json.loads(json.dumps(config.Postdates))  # 不能直接引用
    post_data_raw["name"] = stu_code
    post_data_raw["password"] = password
    headers = {'Referer': 'http://web.weishao.com.cn/login',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.75 Safari/537.36', 'Content-Type': 'application/json'}
    post_data = json.dumps(post_data_raw)  # 这网站必须要先用json.dumps()转换一下，不然验证会失败
    r = requests.post('http://web.weishao.com.cn/api/login', headers=headers, data=post_data)
    result = r.json()
    if not r.ok:
        print('登录失败详细信息:', r.text, end='')
        return None
    return result


# 学号, 密码
def fuck_weishao(stu_code, password):
    if stu_code is None or password is None:
        return False
    answer_data = json.loads(json.dumps(config.Answer))
    totalArr_data = json.loads(json.dumps(config.TotalArr))
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
    for i in range(13, 17):
        totalArr_data[i]['content'] = round(uniform(36.2, 36.9), 1)
    answer_data['totalArr'] = totalArr_data

    # 生成 question_data
    question_data = []
    for i in totalArr_data:
        if i['answered']:
            question_data.append(i)
    answer_data['question_data'] = question_data

    headers = {
        'Referer': 'http://ncp.suse.edu.cn/questionnaire/addanswer?page_from=onpublic&activityid=82&can_repeat=1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; LIO-AN00 Build/HUAWEILIO-AN00; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36 weishao(6.7.4.72570) wsi18n('
                      'zh)',
        'Content-Type': 'application/json'}
    r = requests.post('http://ncp.suse.edu.cn/api/questionnaire/questionnaire/addMyAnswer', headers=headers,
                      data=json.dumps(answer_data))
    if not r.ok:
        print('打卡失败,错误信息如下:', r.text, end='')
        return None
    else:
        return r.json()


# TODO 把user_info和除体温信息外的数据，持久化到本地
if __name__ == '__main__':
    with open('userinfo.csv', mode='r', encoding='gbk') as fp:
        reader = csv.reader(fp)
        all_user_info = {rows[0]: (rows[1], rows[2]) for rows in reader}
    for i in all_user_info.keys():
        if check(i):
            print(all_user_info[i][0], '已打卡')
        else:
            print(all_user_info[i][0], i, all_user_info[i][1], '打卡结果: ', end='')
            print(fuck_weishao(i, all_user_info[i][1]))
