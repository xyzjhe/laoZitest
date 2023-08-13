# coding=utf-8
# !/usr/bin/python
import sys

sys.path.append('..')
from base.spider import Spider
import json
import requests
from requests import session, utils
import os
import time
import base64
from time import strftime
from time import gmtime
import time
time_stamp = str(int(time.time()))
import re
from urllib import request, parse
import urllib.request



class Spider(Spider):  # 元类 默认的元类 type
    box_video_type = ''
    vod_area=''

    def getName(self):
        return "B站个人中心"#自己增加关注pu主和pu主直播(以关注的)


    def __init__(self):


        self.getCookie()



        url = 'http://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=%s&jsonp=jsonp' % (self.userid)

        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)



        fav_list=[]


        if jo['code'] == 0:
            for fav in jo['data'].get('list'):

                fav_dict =  {'n':fav['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"').strip() ,'v':fav['id']}
                fav_list.append(fav_dict)


        if self.config["filter"].get('收藏夹'):
            for i in self.config["filter"].get('收藏夹'):
                if i['key']=='mlid':
                    i['value']=fav_list

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass


    def isVideoFormat(self, url):
        pass

    def second_to_time(self,a):
        #将秒数转化为 时分秒的格式
        if a < 3600:
            return time.strftime("%M:%S", time.gmtime(a))
        else:
            return time.strftime("%H:%M:%S", time.gmtime(a))

    def manualVideoCheck(self):

        pass

    #用户userid
    userid=''

    def get_live_userInfo(self,uid):

        url = 'https://api.live.bilibili.com/live_user/v1/Master/info?uid=%s'%uid


        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)

        if jo['code'] == 0:

            return jo['data']["info"]["uname"]



    def homeContent(self, filter):
        result = {}
        cateManual = {
            "动态": "动态",
            #"关注的pu主":'关注的pu主',
            "直播中":'直播中',

            "收藏夹": '收藏夹',
            "历史记录": '历史记录',
            "稍后再看": '稍后再看',
            '生活直播':'生活直播',
            "热门": "热门",
            
            "排行榜": "排行榜",
            "频道": "频道",
            "直播": "直播",
            "舞蹈": "舞蹈",
            "宅舞": "宅舞",
            "少女": "少女",
            'cosplay':'cosplay',
             'mmd':'mmd',

            "鬼畜": "鬼畜",
            "狗狗": "汪星人",
            '科技': '科技',

            "音声": "音声",
            "演唱会": "演唱会",
            "番剧": "1",
            "国创": "4",
            "电影": "2",
            "综艺": "7",
            "电视剧": "5",
            "纪录片": "3",

        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        self.box_video_type = '热门'
        return self.get_hot(pg='1')

    cookies = ''

    def getCookie(self):

        #放置你的cookies
        rsp=self.fetch("http://127.0.0.1:9978/file/tvboxzz/cookie.txt")
        cookies_str = rsp.text
        if cookies_str:
            cookies =  dict([co.strip().split('=') for co in cookies_str.split(';')])
            bili_jct = cookies['bili_jct']
            SESSDATA = cookies['SESSDATA']
            DedeUserID = cookies['DedeUserID']

            cookies_jar={"bili_jct":bili_jct,
                         'SESSDATA': SESSDATA,
                         'DedeUserID':DedeUserID

            }
            rsp = session()
            rsp.cookies = cookies_jar
            content = self.fetch("http://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
            res = json.loads(content.text)

            if res["code"] == 0:
                self.cookies = rsp.cookies
                self.userid = res["data"].get('mid')

                return rsp.cookies
        rsp = self.fetch("https://www.bilibili.com/")
        self.cookies = rsp.cookies


        return rsp.cookies




    def get_hot(self, pg):
        self.box_video_type = '热门'
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={0}'.format(pg)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
                img = vod['pic'].strip()
                remark = str(self.second_to_time(vod['duration'])).strip()
                videos.append({
                    "vod_id": aid+'&hot',
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def str2sec(self,x):
        '''
          字符串时分秒转换成秒
        '''
        x=str(x)
        try:
              h, m, s = x.strip().split(':') #.split()函数将其通过':'分隔开，.strip()函数用来除去空格
              return int(h)*3600 + int(m)*60 + int(s) #int()函数转换成整数运算
        except:
               m, s = x.strip().split(':') #.split()函数将其通过':'分隔开，.strip()函数用来除去空格
               return  int(m)*60 + int(s) #int()函数转换成整数运算


    def get_rank(self):
        self.box_video_type = '排行榜'
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all'
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
                img = vod['pic'].strip()
                remark = str(self.second_to_time(vod['duration'])).strip()
                videos.append({
                    "vod_id":  aid+'&rank',
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result


    def filter_duration(self, vodlist, key):
        # 按时间过滤
        if key == '0':
            return vodlist
        else:


            vod_list_new = [i for i in vodlist if self.time_diff1[key][0] <= self.str2sec(str(i["vod_remarks"])) < self.time_diff1[key][1]]
            return vod_list_new




    chanel_offset=''
    def get_channel(self, pg, cid,extend,order,duration_diff):
        result = {}
        self.box_video_type = '频道'


        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}&duration={2}&order={3}'.format(
                cid, pg,duration_diff,order)
        rsp = self.fetch(url, cookies=self.cookies)

        content = rsp.text
        jo = json.loads(content)
        if jo.get('code') == 0:
            videos = []
            vodList = jo['data']['result']
            for vod in vodList:
                    aid = str(vod['aid']).strip()
                    title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                    img = 'https:' + vod['pic'].strip()
                    remark = str( self.second_to_time(self.str2sec(vod['duration']))).strip()
                    videos.append({
                        "vod_id":  aid+'&channale',
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })


                #videos=self.filter_duration(videos, duration_diff)
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result




    dynamic_offset = ''

    def get_dynamic(self, pg):
        self.box_video_type = '动态'
        result = {}

        if str(pg) == '1':
            url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page=%s' % pg
        else:
            # print('偏移',self.dynamic_offset)
            url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&offset=%s&page=%s' % (
            self.dynamic_offset, pg)

        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            self.dynamic_offset = jo['data'].get('offset')
            videos = []
            vodList = jo['data']['items']
            for vod in vodList:
                if vod['type'] == 'DYNAMIC_TYPE_AV':
                    #up=vod['modules']["module_author"]['name']
                    ivod = vod['modules']['module_dynamic']['major']['archive']
                    aid = str(ivod['aid']).strip()
                    title = ivod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
                    img = ivod['cover'].strip()
                    #remark = str(ivod['duration_text']).strip()
                    remark =str( self.second_to_time(self.str2sec(ivod['duration_text']))).strip()
                    videos.append({
                        "vod_id": aid+'&dynamic',
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark
                    })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_pu(self,pg):
        result = {}
        if int(pg) > 50:
            return result
        videos = []
        vmid=self.userid
        url= 'https://api.bilibili.com/x/relation/followings?vmid={1}&pn={0}&ps=20&order=desc&order_type=attention'.format(pg,vmid)
        rsp = self.fetch(url, cookies=self.cookies)
        content =rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['mid']).strip()
                title = vod['uname'].strip()
                img = vod['face'].strip()
                remark = str(vod['sign']).strip()
                desc=str(vod['official_verify']['desc']).strip()
                videos.append({
                    "vod_id":title+"###"+aid+"###"+img+"###"+desc+"###"+remark+"&pu",
                    "vod_name":title,
                    "vod_pic":img,
                    "vod_remarks":remark
                })
        numvL = len(videos)
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = int(pg)+1 if numvL>19 else pg
        result['limit'] = numvL
        result['total'] = numvL
        return result

    time_diff1={'1':[0,300],
    '2':[300,900],'3':[900,1800],'4':[1800,3600],
    '5':[3600,99999999999999999999999999999999]

    }

    time_diff='0'


    def get_fav_detail(self,pg,mlid,order):
        result = {}
        self.box_video_type = '收藏夹'



        url = 'http://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&order=%s&pn=%s&ps=20&platform=web&type=0'%(mlid,order,pg)
        rsp = self.fetch(url, cookies=self.cookies)

        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['medias']

            for vod in vodList:
                    #print(vod)
                    #只展示类型为 视频的条目
                    #过滤去掉收藏夹中的 已失效视频;如果不喜欢可以去掉这个 if条件
                    if vod.get('type') in [2]  and vod.get('title') != '已失效视频':

                        aid = str(vod['id']).strip()
                        title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                        img =  vod['cover'].strip()
                        remark = str( self.second_to_time(vod['duration'])).strip()
                        videos.append({
                            "vod_id": aid+'&fav',
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": remark

                        })



                #videos=self.filter_duration(videos, duration_diff)
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999

        return result

    def get_fav(self,pg,order,extend):
        self.box_video_type = '收藏夹'

    #获取自己的up_mid(也就是用户uid)


        mlid=''

        fav_config=self.config["filter"].get('收藏夹')

        #默认显示第一个收藏夹内容
        if fav_config:
            for i in fav_config:
                if i['key']=='mlid':
                    if len(i['value'])>0:
                        mlid=i['value'][0]['v']




        #print(self.config["filter"].get('收藏夹'))

        if 'mlid' in extend:
                mlid = extend['mlid']
        if mlid:
            return self.get_fav_detail(pg=pg,mlid=mlid,order=order)
        else:
            return {}



    def get_history(self,pg):
        result = {}
        self.box_video_type = '历史记录'
        url = 'http://api.bilibili.com/x/v2/history?pn=%s&t=time_stamp' % pg
        rsp = self.fetch(url,cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)   #解析api接口,转化成json数据对象
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']
            for vod in vodList:
                if vod['duration'] > 0:   #筛选掉非视频的历史记录
                    aid = str(vod["aid"]).strip()   #获取 aid
                    #获取标题
                    title = vod["title"].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;",
                                                                                                      '"')
                    #封面图片
                    img = vod["pic"].strip()

                    #获取已观看时间
                    if str(vod['progress'])=='-1':
                        process=str(self.second_to_time(vod['duration'])).strip()
                    else:
                        process = str(self.second_to_time(vod['progress'])).strip()
                    #获取视频总时长
                    total_time= str(self.second_to_time(vod['duration'])).strip()
                    #组合 已观看时间 / 总时长 ,赋值给 remark
                    remark = process+' / '+total_time
                    videos.append({
                        "vod_id":aid+'&history',
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result


    def get_toview(self,pg):
        result = {}
        self.box_video_type = '稍后再看'
        url = 'http://api.bilibili.com/x/v2/history/toview'
        rsp = self.fetch(url,cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)   #解析api接口,转化成json数据对象
        if jo['code'] == 0:
            videos = []
            vodList = jo['data'].get('list')

            for vod in vodList:

                if vod['duration'] > 0:   #筛选掉非视频的历史记录
                    aid = str(vod["aid"]).strip()   #获取 aid
                    #获取标题
                    title = vod["title"].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;",
                                                                                                      '"')
                    #封面图片
                    img = vod["pic"].strip()

                    #获取已观看时间
                    if str(vod['progress'])=='-1':
                        process=str(self.second_to_time(vod['duration'])).strip()
                    else:
                        process = str(self.second_to_time(vod['progress'])).strip()
                    #获取视频总时长
                    total_time= str(self.second_to_time(vod['duration'])).strip()
                    #组合 已观看时间 / 总时长 ,赋值给 remark
                    remark = process+' / '+total_time
                    videos.append({
                        "vod_id":aid+'&toview',
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = pg
            result['limit'] = len(videos)
            result['total'] = len(videos)
        return result


    def get_live(self,pg,parent_area_id,area_id):
        result = {}
        self.box_video_type = '直播'


        url = 'https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=%s&area_id=%s&sort_type=online&page=%s'%(parent_area_id,area_id,pg)
        rsp = self.fetch(url, cookies=self.cookies)

        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']

            for vod in vodList:



                        aid = str(vod['roomid']).strip()
                        title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                        img =  vod.get('cover').strip()
                        remark = '直播间人数:'+str( vod['online']).strip()
                        videos.append({
                            "vod_id": aid+'&live',
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": remark

                        })



                #videos=self.filter_duration(videos, duration_diff)
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999

        return result
    def get_live_goodFor(self,pg):
        result = {}
        self.box_video_type = '直播'
        ts=str(int(time.time()*1000))
        url = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/xfetter/GetWebList?page={0}&page_size=10&_={1}'.format(pg,ts)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                        aid = str(vod['room_id']).strip()
                        title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                        img =  vod.get('keyframe').strip()
                        remark = '直播间人数:'+str( vod['online']).strip()
                        videos.append({
                            "vod_id": aid+'&live',
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": remark
                        })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = int(pg)+1 if len(videos)==10 else int(pg)
            result['limit'] = 90
            result['total'] = 999999
        return result
    def categoryContent(self, tid, pg, filter, extend):

        result = {}

        if len(self.cookies) <= 0:
            self.getCookie()

        if tid == "热门":
            self.box_video_type = '热门'
            return self.get_hot(pg=pg)
        elif tid == "关注的pu主":
            self.box_video_type = '关注的pu主'
            return self.get_pu(pg=pg)
        elif tid == "排行榜":
            self.box_video_type = '排行榜'
            return self.get_rank()
        elif tid== '稍后再看':
            self.box_video_type = '稍后再看'
            return self.get_toview(pg)

        elif tid == "收藏夹":
            self.box_video_type = '收藏夹'
            order = 'mtime'
            if 'order' in extend:
                order = extend['order']

            return self.get_fav(pg=pg, order=order,extend=extend)
            
            
        elif tid == '生活直播':
            self.box_video_type = '直播'
            parent_area_id = '10'
            area_id=''
            if 'area_id' in extend:
                area_id = extend['area_id']
            return  self.get_live(pg=pg,parent_area_id=parent_area_id,area_id=area_id)

        elif tid == '直播':
            self.box_video_type = '直播'
            parent_area_id = '1'
            if 'parent_area_id' in extend:
                parent_area_id = extend['parent_area_id']
            return  self.get_live(pg=pg,parent_area_id=parent_area_id,area_id='')

        
        elif tid == '直播中':
            self.box_video_type = '直播'
            return  self.get_live_goodFor(pg=pg)

        elif tid == '频道':
            self.box_video_type = '频道'

            cid = '搞笑'
            if 'cid' in extend:
                cid = extend['cid']

            duration_diff='0'
            if 'duration' in extend:
                duration_diff = extend['duration']

            order = 'totalrank'
            if 'order' in extend:
                order = extend['order']






            return self.get_channel(pg=pg, cid=cid,extend=extend,order=order,duration_diff=duration_diff)


        elif tid == '动态':
            self.box_video_type = '动态'
            return self.get_dynamic(pg=pg)

        elif tid == '历史记录':
            self.box_video_type = '历史记录'
            return self.get_history(pg=pg)
        elif tid.isdigit():
            self.box_video_type = '影视'
            url = 'https://api.bilibili.com/pgc/season/index/result?order=2&season_status=-1&style_id=-1&sort=0&area=-1&pagesize=20&type=1&st={0}&season_type={0}&page={1}'.format(
                tid, pg)
            rsp = self.fetch(url, cookies=self.cookies)
            content = rsp.text
            jo = json.loads(content)
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['cover'].strip()
                remark = vod['index_show'].strip()
                videos.append({
                    "vod_id": aid+'&movie',
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark  # 视频part数量

                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999



        else:
            duration_diff='0'
            if 'duration' in extend:
                duration_diff = extend['duration']

            order = 'totalrank'
            if 'order' in extend:
                order = extend['order']




            self.box_video_type = '其他'
            url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}&duration={2}&order={3}'.format(
                tid, pg,duration_diff,order)
            rsp = self.fetch(url, cookies=self.cookies)

            content = rsp.text
            jo = json.loads(content)

            if jo.get('code') == 0:
                videos = []
                vodList = jo['data']['result']
                for vod in vodList:
                    aid = str(vod['aid']).strip()
                    title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                    img = 'https:' + vod['pic'].strip()
                    #remark = str(vod['duration']).strip()
                    remark =str( self.second_to_time(self.str2sec(vod['duration']))).strip()
                    videos.append({
                        "vod_id": aid+'&other',
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })


            #videos=self.filter_duration(videos, duration_diff)
                result['list'] = videos
                result['page'] = pg
                result['pagecount'] = 9999
                result['limit'] = 90
                result['total'] = 999999
        return result

    def cleanSpace(self, str):
        return str.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    def detailContent(self, array):
        # if int(array[0])< 1000000:
        result={}
        arrays =  array[0].split("&")
        if arrays[-1] == 'movie':
            self.box_video_type='影视'
            aid = arrays[0]
            url = "http://api.bilibili.com/pgc/view/web/season?season_id={0}".format(aid)
            rsp = self.fetch(url, headers=self.header)
            jRoot = json.loads(rsp.text)
            if jRoot['code'] == 0:
                jo = jRoot['result']
                id = jo['season_id']
                title = jo['title']
                pic = jo['cover']
                areas = jo['areas'][0]['name']
                typeName = jo['share_sub_title']
                dec = jo['evaluate']
                remark = jo['new_ep']['desc']
                vod = {
                    "vod_id": array[0],
                    "vod_name": title,
                    "vod_pic": pic,
                    "type_name": typeName,
                    "vod_year": "",
                    # "vod_area":areas,
                    "vod_area": self.vod_area,  #弹幕是否显示的开关
                    "vod_remarks": remark,
                    "vod_actor": "",
                    "vod_director": "",
                    "vod_content": dec
                }
                ja = jo['episodes']
                playUrl = ''
                for tmpJo in ja:
                    eid = tmpJo['id']
                    cid = tmpJo['cid']
                    part = tmpJo['title'].replace("#", "-")
                    playUrl = playUrl + '{0}${1}_{2}#'.format(part, eid, cid)

                vod['vod_play_from'] = 'B站'
                vod['vod_play_url'] = playUrl

                result = {
                    'list': [
                        vod
                    ]
                }

        elif arrays[-1] == 'live':
            self.box_video_type='直播'
            aid = arrays[0]


            url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s"%aid
            rsp = self.fetch(url, headers=self.header,cookies=self.cookies)
            jRoot = json.loads(rsp.text)
            if jRoot.get('code')==0:
                jo = jRoot['data']
                title = jo['title'].replace("<em class=\"keyword\">", "").replace("</em>", "")
                pic = jo.get("user_cover")
                desc = jo.get('description')

                dire = self.get_live_userInfo(jo["uid"])
                typeName = jo.get("area_name")
                remark = '在线人数:'+str(jo['online']).strip()

                vod = {
                    "vod_id": aid+"&live",
                    "vod_name": '(' + dire + ")" + title,
                    "vod_pic": pic,
                    "type_name": typeName,

                    "vod_area": self.vod_area,
                     #"vod_area":"",
                    "vod_remarks": remark,
                    "vod_actor": "直播间id-"+aid,
                    "vod_director": dire,
                    "vod_content": desc + '\n主播:' + dire,
                    'vod_play_from':'B站',
                    'vod_play_url':'flv线路原画$platform=web&quality=4_'+aid+'#flv线路高清$platform=web&quality=3_'+aid+'#h5线路原画$platform=h5&quality=4_'+aid+'#h5线路高清$platform=h5&quality=3_'+aid
                   #  'vod_play_url':aid
                }


                result = {
                    'list': [
                        vod
                    ]
                }
        elif arrays[-1] == 'pu':
            self.box_video_type='pu'
            aidList=arrays[0].split('###')
            title = aidList[0]
            mid=aidList[1]
            pic = aidList[2]
            videoList=[]
            m=2
            if mid=='72270557':
                m=8
            for i in range(1, m):
                url = "https://api.bilibili.com/x/space/wbi/arc/search?mid={0}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1bab351d584ef97b4d0bb3024acce02d&wts=1684745027".format(mid,i)
                rsp = self.fetch(url,headers=self.header)
                htmlTxt= rsp.text
                jRoot = json.loads(htmlTxt)
                jo = jRoot['data']
                ja = jo['list']
                videos=ja['vlist']
                if len(videos)<1:
                    break
                for tmpJo in videos:
                    vodTitle = tmpJo['title']
                    bvid = tmpJo['bvid']
                    videoList.append(vodTitle+"$"+'bvid:'+bvid)
            typeName = aidList[3]
            remark = aidList[4].replace("&pu","")
            vod = {
                "vod_id": title+"###"+mid+"###"+pic+"###"+typeName+"###"+remark+"&pu",
                "vod_name": title,
                "vod_pic": pic,
                "type_name": typeName,
                "vod_year": '',
                "vod_area": "",
                "vod_remarks": '',
                "vod_actor": "",
                "vod_director": '',
                "vod_content": remark
            }
            playUrl="#"
            if len(videoList)>0:
                playUrl="#".join(videoList)
            vod['vod_play_from'] = 'B站视频'
            vod['vod_play_url'] = playUrl

            result = {
                'list': [
                    vod
                ]
            }
        else :
            self.box_video_type='其他'
            aid = arrays[0]
            url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)
            rsp = self.fetch(url, headers=self.header)
            jRoot = json.loads(rsp.text)
            if jRoot['code'] == 0:
                jo = jRoot['data']
                title = jo['title'].replace("<em class=\"keyword\">", "").replace("</em>", "")
                pic = jo['pic']
                desc = jo['desc']
                timeStamp = jo['pubdate']
                timeArray = time.localtime(timeStamp)
                year = str(time.strftime("%Y", timeArray))
                dire = jo['owner']['name']
                typeName = jo['tname']
                remark = str(jo['duration']).strip()

                vod = {
                    "vod_id": aid,
                    "vod_name": '(' + dire + ")" + title,
                    "vod_pic": pic,
                    "type_name": typeName,
                    "vod_year": year,
                    "vod_area": self.vod_area,
                    # "vod_area":"",
                    "vod_remarks": remark,
                   
                    'vod_tags':'mv',

                    "vod_director": dire,
                    "vod_content": desc + '\nup主:' + dire
                }
                ja = jo['pages']
                playUrl = ''
                for tmpJo in ja:
                    cid = tmpJo['cid']
                    part = tmpJo['part'].replace("#", "-")
                    playUrl = playUrl + '{0}${1}_{2}#'.format(part, aid, cid)

                vod['vod_play_from'] = 'B站'
                vod['vod_play_url'] = playUrl

                result = {
                    'list': [
                        vod
                    ]
                }
        return result
    

    def searchContent(self, key, quick):
        videos=[]
        isPU=False
        if len(key)>3 and key.find('-PU')>1:
            key=key[0:len(key)-3]
            isPU=True
        videos = self.get_search(key=key)
        temporary=self.get_search_Movies(key=key)
        for vod in temporary:
            videos.append(vod)
        temporary=self.get_search_Fanju(key=key)
        for vod in temporary:
            videos.append(vod)
        #if isPU=True:
            temporary=self.get_search_PU(key=key)
            for vod in temporary:
                videos.append(vod)
        result = {
            'list': videos
        }
        return result
        #番剧搜索
    def get_search_Fanju(self, key):
        self.box_video_type = '搜索'
        header = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/web-interface/search/type?keyword={0}&page=1&search_type=media_bangumi&order=totalrank&pagesize=20'.format(urllib.parse.quote(key))

        rsp = self.fetch(url, cookies=self.cookies, headers=header)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:
            return []
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
            img = vod['cover'].strip()
            remark = str(vod['desc']).strip()
            videos.append({
               "vod_id": aid+'&movie',
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        return videos
        #PU搜索
    def get_search_PU(self, key):
        self.box_video_type = '搜索'
        header = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/web-interface/search/type?keyword={0}&page=1&search_type=bili_user&order=totalrank&pagesize=20'.format(urllib.parse.quote(key))

        rsp = self.fetch(url, cookies=self.cookies, headers=header)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:
            return []
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['mid']).strip()
            title = vod['uname'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
            img = 'https://'+vod['upic'].strip()
            remark = str(vod['usign']).strip()
            videos.append({
               "vod_id": aid+'&pu',
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        return videos
        #视频搜索
    def get_search(self, key):
        self.box_video_type = '搜索'
        header = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page=1'.format(key)

        rsp = self.fetch(url, cookies=self.cookies, headers=header)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:
            rspRetry = self.fetch(url, cookies=self.cookies, headers=header)
            content = rspRetry.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['aid']).strip()
            title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
            img = 'https:' + vod['pic'].strip()
            remark = str(vod['duration']).strip()
            videos.append({
               "vod_id": aid+'&search',
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        return videos
        #影视搜索
    def get_search_Movies(self, key):
        self.box_video_type = '搜索'
        header = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/web-interface/search/type?keyword={0}&page=1&search_type=media_ft&order=totalrank&pagesize=20'.format(urllib.parse.quote(key))

        rsp = self.fetch(url, cookies=self.cookies, headers=header)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:
            return []
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
            img = vod['cover'].strip()
            remark = str(vod['desc']).strip()
            videos.append({
               "vod_id": aid+'&movie',
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        return videos

    def playerContent(self, flag, id, vipFlags):
        result = {}

        avId=''
        try:
            if self.box_video_type == '影视':
                ids = id.split("_")
                avId="av"+ids[0]
                #return self.Get_vip(ep=ids[0])#直接调用vip解析,如果是vip账号请删除
                header = {
                    "Referer": "https://www.bilibili.com",
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
                }
                url = 'https://api.bilibili.com/pgc/player/web/playurl?qn=116&ep_id={0}&cid={1}'.format(ids[0], ids[1])
                if len(self.cookies) <= 0:
                    self.getCookie()
                rsp = self.fetch(url, cookies=self.cookies, headers=header)
                jRoot = json.loads(rsp.text)
                if jRoot['message'] != 'success':
                    print("需要大会员权限才能观看")
                    return result
                jo = jRoot['result']
                ja = jo['durl']
                maxSize = -1
                position = -1
                for i in range(len(ja)):
                    tmpJo = ja[i]
                    if maxSize < int(tmpJo['size']):
                        maxSize = int(tmpJo['size'])
                        position = i

                url = ''
                if len(ja) > 0:
                    if position == -1:
                        position = 0
                    url = ja[position]['url']

                result["parse"] = 0
                result["playUrl"] = ''
                result["url"] = url
                result["header"] = {
                    "Referer": "https://www.bilibili.com",
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
                }
                result["contentType"] = 'video/x-flv'
                

            elif self.box_video_type == '直播':

                ids = id.split("_")


                url = 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&%s'%(ids[1],ids[0])

                #raise Exception(url)
                if len(self.cookies) <= 0:
                    self.getCookie()
                rsp = self.fetch(url, cookies=self.cookies)
                jRoot = json.loads(rsp.text)


                if jRoot['code'] == 0:


                    jo = jRoot['data']
                    ja = jo['durl']


                    url = ''
                    if len(ja) > 0:

                        url = ja[0]['url']

                    result["parse"] = 0
                    # result['type'] ="m3u8"
                    result["playUrl"] = ''

                    result["url"] = url
                    result["header"] = {
                        "Referer": "https://live.bilibili.com",
                        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
                    }


                    
                    if "h5" in ids[0]:
                        result["contentType"] = ''
                    else:
                        result["contentType"] = 'video/x-flv'
            elif self.box_video_type == 'pu':
                avId=mark=id.split(":")[1]
                result = self.get_Url_pu(idTxt=id)
            else:

                ids = id.split("_")
                avId="av"+ids[0]
                url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid={1}&qn=116'.format(ids[0], ids[1])

                if len(self.cookies) <= 0:
                    self.getCookie()
                rsp = self.fetch(url, cookies=self.cookies)
                jRoot = json.loads(rsp.text)
                jo = jRoot['data']
                ja = jo['durl']

                maxSize = -1
                position = -1

                for i in range(len(ja)):
                    tmpJo = ja[i]
                    if maxSize < int(tmpJo['size']):
                        maxSize = int(tmpJo['size'])
                        position = i

                url = ''
                if len(ja) > 0:
                    if position == -1:
                        position = 0
                    url = ja[position]['url']

                result["parse"] = 0
                result["playUrl"] = ''
                result["url"] = url
                result["header"] = {
                    "Referer": "https://www.bilibili.com",
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
                }
                result["contentType"] = 'video/x-flv'
        except Exception as e:
            print(e)
            result={}
        if result=={} and self.box_video_type.find('直播')<0:
            result= self.get_mp4(av=avId)  
        return result
    def Get_vip(self,ep):
        url='https://www.bilibili.com/bangumi/play/ep{0}'.format(ep)
        result={}
        result["parse"] = 1
        result['jx'] = 1
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = ''
        return result
    def get_mp4(self,av):
        result={}
        url='https://m.bilibili.com/video/{0}'.format(av)
        header1= {
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Mobile Safari/537.36"
        }
        rsp=self.fetch(url,headers=header1)
        html=rsp.text
        url=self.get_RegexGetText(Text=html,RegexText=r'"readyVideoUrl":"(.+?)","readyDuration":',Index=1)
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = header1
        return result
    def get_RegexGetText(self,Text,RegexText,Index):
        returnTxt=""
        Regex=re.search(RegexText, Text, re.M|re.S)
        if Regex is not None:
            returnTxt=Regex.group(Index)
        return returnTxt    
    def get_Url_pu(self,idTxt):
        result = {}
        ids = idTxt.split(":")
        header = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        url = 'https://api.bilibili.com/x/web-interface/view?bvid={0}'.format(ids[1])
        rsp =self.fetch(url, headers=header)
        jRoot = json.loads(rsp.text)
        jo = jRoot['data']
        aid=jo['aid']
        cid=jo['cid']
        url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid={1}&qn=120&fnval=0&128=128&fourk=1'.format(aid,cid)
        rsp = self.fetch(url, headers=header)
        jRoot = json.loads(rsp.text)
        jo = jRoot['data']
        if jRoot['code']!=0:
            return result
        ja = jo['durl']
        maxSize = -1
        position = -1
        for i in range(len(ja)):
            tmpJo = ja[i]
            if maxSize < int(tmpJo['size']):
                maxSize = int(tmpJo['size'])
                position = i
        url = ''
        if len(ja) > 0:
            if position == -1:
                position = 0
            url = ja[position]['url']
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["contentType"] = 'video/x-flv'
        result["header"] = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        return result
    config = {
        "player": {},
        "filter": {



        "舞蹈": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],



         "少女": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],

         "mmd": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],

            "直播": [{
                "key": "parent_area_id",
                "name": "直播分区",
                "value": [

                 

                    {
                        "n": "娱乐",
                        "v": "1"
                    },
                    {
                        "n": "电台",
                        "v": "5"
                    },
                    {
                        "n": "网游",
                        "v": "2"
                    },
                     {
                        "n": "手游",
                        "v": "3"
                    },



                     {
                        "n": "单机游戏",
                        "v": "6"
                    },

                     {
                        "n": "虚拟主播",
                        "v": "9"
                    },{'n': '生活', 'v': 10},
                    {'n': '知识', 'v': 11},
                    {'n': '赛事', 'v': 13}



                ]
            },
                ],
                
                
                "生活直播":[{"key":"area_id","name":"小分区","value":[{"n":"生活分享","v":"646"},{"n":"运动","v":"628"},{"n":"搞笑","v":"624"},{"n":"手工绘画","v":"627"},{"n":"萌宠","v":"369"},{"n":"美食","v":"367"},{"n":"时尚","v":"378"},{"n":"影音馆","v":"33"}] }],


         "音声": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],

         "收藏夹": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "收藏时间",
                        "v": "mtime"
                    },

                    {
                        "n": "播放量",
                        "v": "view"
                    },

                    {
                        "n": "投稿时间",
                        "v": "pubtime"
                    }



                ]
            },
                {
                    "key": "mlid",
                    "name": "收藏夹分区",
                    "value": [
                    ]
                }],
         "cosplay": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],





















            "频道": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }, {"key": "cid", "name": "分类",
                    "value":[{'n': '搞笑', 'v': '搞笑'}, {'n': '美食', 'v': '美食'}, {'n': '鬼畜', 'v': '鬼畜'}, {'n': '美妆', 'v': '美妆'}, {'n': 'mmd', 'v': 'mmd'}, {'n': '科普', 'v': '科普'}, {'n': 'COSPLAY', 'v': 'COSPLAY'}, {'n': '漫展', 'v': '漫展'}, {'n': 'MAD', 'v': 'MAD'}, {'n': '手书', 'v': '手书'}, {'n': '穿搭', 'v': '穿搭'}, {'n': '发型', 'v': '发型'}, {'n': '化妆教程', 'v': '化妆教程'}, {'n': '电音', 'v': '电音'}, {'n': '欧美音乐', 'v': '欧美音乐'}, {'n': '中文翻唱', 'v': '中文翻唱'}, {'n': '洛天依', 'v': '洛天依'}, {'n': '翻唱', 'v': '翻唱'}, {'n': '日文翻唱', 'v': '日文翻唱'}, {'n': '科普', 'v': '科普'}, {'n': '技术宅', 'v': '技术宅'}, {'n': '历史', 'v': '历史'}, {'n': '科学', 'v': '科学'}, {'n': '人文', 'v': '人文'}, {'n': '科幻', 'v': '科幻'}, {'n': '手机', 'v': '手机'}, {'n': '手机评测', 'v': '手机评测'}, {'n': '电脑', 'v': '电脑'}, {'n': '摄影', 'v': '摄影'}, {'n': '笔记本', 'v': '笔记本'}, {'n': '装机', 'v': '装机'}, {'n': '课堂教育', 'v': '课堂教育'}, {'n': '公开课', 'v': '公开课'}, {'n': '演讲', 'v': '演讲'}, {'n': 'PS教程', 'v': 'PS教程'}, {'n': '编程', 'v': '编程'}, {'n': '英语学习', 'v': '英语学习'}, {'n': '喵星人', 'v': '喵星人'}, {'n': '萌宠', 'v': '萌宠'}, {'n': '汪星人', 'v': '汪星人'}, {'n': '大熊猫', 'v': '大熊猫'}, {'n': '柴犬', 'v': '柴犬'},{'n': '田园犬', 'v': '田园犬'}, {'n': '吱星人', 'v': '吱星人'}, {'n': '美食', 'v': '美食'}, {'n': '甜点', 'v': '甜点'}, {'n': '吃货', 'v': '吃货'}, {'n': '厨艺', 'v': '厨艺'}, {'n': '烘焙', 'v': '烘焙'}, {'n': '街头美食', 'v': '街头美食'}, {'n': 'A.I.Channel', 'v': 'A.I.Channel'}, {'n': '虚拟UP主', 'v': '虚拟UP主'}, {'n': '神楽めあ', 'v': '神楽めあ'}, {'n': '白上吹雪', 'v': '白上吹雪'}, {'n': '婺源', 'v': '婺源'}, {'n': 'hololive', 'v': 'hololive'}, {'n': 'EXO', 'v': 'EXO'}, {'n': '防弹少年团', 'v': '防弹少年团'}, {'n': '肖战', 'v': '肖战'}, {'n': '王一博', 'v': '王一博'}, {'n': '易烊千玺', 'v': '易烊千玺'}, {'n': '赵今麦', 'v': '赵今麦'}, {'n': '宅舞', 'v': '宅舞'}, {'n': '街舞', 'v': '街舞'}, {'n': '舞蹈教学', 'v': '舞蹈教学'}, {'n': '明星舞蹈', 'v': '明星舞蹈'}, {'n': '韩舞', 'v': '韩舞'}, {'n': '古典舞', 'v': '古典舞'}, {'n': '旅游', 'v': '旅游'}, {'n': '绘画', 'v': '绘画'}, {'n': '手工', 'v': '手工'}, {'n': 'vlog', 'v': 'vlog'}, {'n': 'DIY', 'v': 'DIY'}, {'n': '手绘', 'v': '手绘'}, {'n': '综艺', 'v': '综艺'}, {'n': '国家宝藏', 'v': '国家宝藏'}, {'n': '脱口秀', 'v': '脱口秀'}, {'n': '日本综艺', 'v': '日本综艺'}, {'n': '国内综艺', 'v': '国内综艺'}, {'n': '人类观察', 'v': '人类观察'}, {'n': '影评', 'v': '影评'}, {'n': '电影解说', 'v': '电影解说'}, {'n': '影视混剪', 'v': '影视混剪'}, {'n': '影视剪辑', 'v': '影视剪辑'}, {'n': '漫威', 'v': '漫威'}, {'n': '超级英雄', 'v': '超级英雄'}, {'n': '影视混剪', 'v': '影视混剪'}, {'n': '影视剪辑', 'v': '影视剪辑'},
                             {'n': '诸葛亮', 'v': '诸葛亮'}, {'n': '韩剧', 'v': '韩剧'}, {'n': '王司徒', 'v': '王司徒'}, {'n': '泰剧', 'v': '泰剧'},
                             {'n': '郭德纲', 'v': '郭德纲'}, {'n': '相声', 'v': '相声'}, {'n': '张云雷', 'v': '张云雷'}, {'n': '秦霄贤', 'v': '秦霄贤'}, {'n': '孟鹤堂', 'v': '孟鹤堂'}, {'n': '岳云鹏', 'v': '岳云鹏'}, {'n': '假面骑士', 'v': '假面骑士'}, {'n': '特摄', 'v': '特摄'}, {'n': '奥特曼', 'v': '奥特曼'}, {'n': '迪迦奥特曼', 'v': '迪迦奥特曼'}, {'n': '超级战队', 'v': '超级战队'}, {'n': '铠甲勇士', 'v': '铠甲勇士'}, {'n': '健身', 'v': '健身'}, {'n': '篮球', 'v': '篮球'}, {'n': '体育', 'v': '体育'}, {'n': '帕梅拉', 'v': '帕梅拉'}, {'n': '极限运动', 'v': '极限运动'}, {'n': '足球', 'v': '足球'}, {'n': '星海', 'v': '星海'}, {'n': '张召忠', 'v': '张召忠'}, {'n': '航母', 'v': '航母'}, {'n': '航天', 'v': '航天'}, {'n': '导弹', 'v': '导弹'}, {'n': '战斗机', 'v': '战斗机'}]
}
            ],
        }
    }
    header = {
                "Referer": "https://www.bilibili.com",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }

    def localProxy(self, param):


        return [200, "video/MP2T", action, ""]


if __name__ == '__main__':
    a=Spider()
    print(time_stamp)

    print(a.categoryContent('5','1',filter={},extend='1'))


    #print(a.get_live(pg=1,parent_area_id='0'))

    a.box_video_type='直播'
    print(a.get_hot(pg=1))
    print(a.detailContent(['43000&movie']))


    print(a.get_toview(1))



    #print(a.get_fav(pg='1',order='mtime',extend={}))
