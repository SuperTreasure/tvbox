#coding=utf-8
#!/usr/bin/python
import re
import sys

import requests

sys.path.append('..')
from base.spider import Spider
import json


class Spider(Spider):

    def getName(self):
        return "斗鱼"

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {"热门游戏": "热门游戏", "主机游戏": "主机游戏", "原创IP": "原创IP"}
        classes = []
        for k in cateManual:
            classes.append({'type_name': k, 'type_id': cateManual[k]})

        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        result = {}
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        url = 'http://live.yj1211.work/api/live/getRecommendByPlatformArea?platform=douyu&size=20&area={0}&page={1}'.format(
            tid, pg)
        rsp = self.fetch(url)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']
        for vod in vodList:
            aid = (vod['roomId']).strip()
            title = vod['roomName'].strip()
            # img = vod['roomPic'].strip()
            img = vod['ownerHeadPic'].strip()
            remark = (vod['ownerName']).strip()
            videos.append({"vod_id": aid, "vod_name": title, "vod_pic": img, "vod_remarks": remark})
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, array):
        aid = array[0]
        url = "http://live.yj1211.work/api/live/getRoomInfo?platform=douyu&roomId={0}".format(aid)
        rsp = self.fetch(url)
        jRoot = json.loads(rsp.text)
        jo = jRoot['data']
        title = jo['roomName']
        pic = jo['roomPic']
        desc = str(jo['online'])
        dire = jo['ownerName']
        typeName = jo['categoryName']
        remark = jo['categoryName']
        vod = {
            "vod_id": aid,
            "vod_name": title,
            "vod_pic": pic,
            "type_name": typeName,
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": remark,
            "vod_actor": '在线人数:' + desc,
            "vod_director": dire,
            "vod_content": ""
        }
        playUrl = '原画' + '${0}#'.format(aid)
        vod['vod_play_from'] = '斗鱼直播'
        vod['vod_play_url'] = playUrl

        result = {'list': [vod]}
        return result

    def searchContent(self, key, quick):
        result = {}
        url = "http://live.yj1211.work/api/live/search?platform=douyu&keyWords={0}&uid=5774c214491e41418d18f5438855668c".format(
            key)
        rsp = self.fetch(url=url)
        jRoot = json.loads(rsp.text)
        vodList = jRoot['data']
        videos = []
        for vod in vodList:
            aid = (vod['roomId']).strip()
            title = vod['nickName'].strip()
            img = vod['headPic'].strip()
            remark = ('在线人数: ' + str(vod['followers'])).strip()
            videos.append({"vod_id": aid, "vod_name": title, "vod_pic": img, "vod_remarks": remark})
        result = {'list': videos}
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}

        # res = requests.get("https://api.ezong.love/douyu?id={0}".format(id))
        # url = re.findall(r'<br /><br />(.*?)</div>',res.text,re.S)[0]

        url = 'http://live.yj1211.work/api/live/getRealUrlMultiSource?platform=douyu&roomId={0}'.format(id)
        rsp = self.fetch(url=url)
        jRoot = json.loads(rsp.text)
        for jo in jRoot['data']:
            for dict in jRoot['data'][jo]:
                url = dict['playUrl']
                break

        # url = 'https://getplayurl.lmteam.repl.co/live?platform=douyu&rid={0}'.format(id)
        # rsp = requests.get(url, allow_redirects=False)
        # if 'Location' in rsp.headers:
        # 	url = rsp.headers['Location']
        # else:
        # 	url = ''

        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = ''
        return result

    config = {"player": {}, "filter": {}}
    header = {}

    def localProxy(self, param):
        action = {'url': '', 'header': '', 'param': '', 'type': 'string', 'after': ''}
        return [200, "video/MP2T", action, ""]
