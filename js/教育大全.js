/* 直播弹幕 -> vod_area:'bilidanmu'
目前只有皮皮虾大佬的DMBox, 支持弹幕
DMBox下载:https://t.me/pipixiawerun
设置 > 窗口预览 > 开启
*/

/* Cookie设置
Cookie改为预设获取蜂蜜大佬Github的
https://github.com/FongMi/CatVodSpider/raw/main/txt/cookie.txt

Cookie获取方法
https://github.com/UndCover/PyramidStore/blob/main/list.md#%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9

Cookie设置方法1: DR-PY 后台管理界面
CMS后台管理 > 设置中心 > 环境变量 > {"bili_cookie":"XXXXXXX","vmid":"XXXXXX"} > 保存

Cookie设置方法2: 手动替换Cookie
底下代码 headers的
"Cookie":"$bili_cookie"
手动替换为
"Cookie":"将获取的Cookie黏贴在这"
*/

var rule = {
    title:'我的哔哩',
    host:'https://api.bilibili.com',
    homeUrl:'/x/web-interface/search/type?search_type=video&keyword=小姐姐4K&page=1',
    url:'/x/web-interface/search/type?search_type=videofyfilter',
    class_name:'1年级语文&1年级数学&1年级英语&2年级语文&2年级数学&2年级英语&3年级语文&3年级数学&3年级英语&4年级语文&4年级数学&4年级英语&5年级语文&5年级数学&5年级英语&6年级语文&6年级数学&6年级英语',
    class_url:'1年级语文&1年级数学&1年级英语&2年级语文&2年级数学&2年级英语&3年级语文&3年级数学&3年级英语&4年级语文&4年级数学&4年级英语&5年级语文&5年级数学&5年级英语&6年级语文&6年级数学&6年级英语',
    filterable: 1,
    filter_url: '&keyword={{fl.tid}}&page=fypage&duration={{fl.duration}}&order={{fl.order}}',
    filter_def:
      {
        1年级语文:{tid:'1年级语文'},
        1年级数学:{tid:'1年级数学'},
        1年级英语:{tid:'1年级英语'},
        2年级语文:{tid:'2年级语文'},
        2年级数学:{tid:'2年级数学'},
        2年级英语:{tid:'2年级英语'},
        3年级语文:{tid:'3年级语文'},
        3年级数学:{tid:'3年级数学'},
        3年级英语:{tid:'3年级英语'},
        4年级语文:{tid:'4年级语文'},
        4年级数学:{tid:'4年级数学'},
        4年级英语:{tid:'4年级英语'},
        5年级语文:{tid:'5年级语文'},
        5年级数学:{tid:'5年级数学'},
        5年级英语:{tid:'5年级英语'},
        6年级语文:{tid:'6年级语文'},
        6年级数学:{tid:'6年级数学'},
        6年级英语:{tid:'6年级英语'}
         },
    filter: 
  {
  	  
"1年级语文": 
[
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "1年级语文"},
{"n": "沪教版","v": "沪教版1年级语文"},
{"n": "人教版","v": "人教版1年级语文"},
{"n": "北师大版","v": "北师大版1年级语文"},
{"n": "苏教版","v": "苏教版1年级语文"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"1年级英语": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "1年级英语"},
{"n": "沪教版","v": "沪教版1年级英语"},
{"n": "人教版","v": "人教版1年级英语"},
{"n": "北师大版","v": "北师大版1年级英语"},
{"n": "苏教版","v": "苏教版1年级英语"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"1年级数学": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "1年级数学"},
{"n": "沪教版","v": "沪教版1年级数学"},
{"n": "人教版","v": "人教版1年级数学"},
{"n": "北师大版","v": "北师大版1年级数学"},
{"n": "苏教版","v": "苏教版1年级数学"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"2年级语文": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "2年级语文"},
{"n": "沪教版","v": "沪教版2年级语文"},
{"n": "人教版","v": "人教版2年级语文"},
{"n": "北师大版","v": "北师大版2年级语文"},
{"n": "苏教版","v": "苏教版2年级语文"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"2年级英语": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "2年级英语"},
{"n": "沪教版","v": "沪教版2年级英语"},
{"n": "人教版","v": "人教版2年级英语"},
{"n": "北师大版","v": "北师大版2年级英语"},
{"n": "苏教版","v": "苏教版2年级英语"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"2年级数学": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "2年级数学"},
{"n": "沪教版","v": "沪教版2年级数学"},
{"n": "人教版","v": "人教版2年级数学"},
{"n": "北师大版","v": "北师大版2年级数学"},
{"n": "苏教版","v": "苏教版2年级数学"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"3年级语文": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "3年级语文"},
{"n": "沪教版","v": "沪教版3年级语文"},
{"n": "人教版","v": "人教版3年级语文"},
{"n": "北师大版","v": "北师大版3年级语文"},
{"n": "苏教版","v": "苏教版3年级语文"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"3年级英语": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "3年级英语"},
{"n": "沪教版","v": "沪教版3年级英语"},
{"n": "人教版","v": "人教版3年级英语"},
{"n": "北师大版","v": "北师大版3年级英语"},
{"n": "苏教版","v": "苏教版3年级英语"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"3年级数学": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "3年级数学"},
{"n": "沪教版","v": "沪教版3年级数学"},
{"n": "人教版","v": "人教版3年级数学"},
{"n": "北师大版","v": "北师大版3年级数学"},
{"n": "苏教版","v": "苏教版3年级数学"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"4年级语文": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "4年级语文"},
{"n": "沪教版","v": "沪教版4年级语文"},
{"n": "人教版","v": "人教版4年级语文"},
{"n": "北师大版","v": "北师大版4年级语文"},
{"n": "苏教版","v": "苏教版4年级语文"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"4年级英语": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "4年级英语"},
{"n": "沪教版","v": "沪教版4年级英语"},
{"n": "人教版","v": "人教版4年级英语"},
{"n": "北师大版","v": "北师大版4年级英语"},
{"n": "苏教版","v": "苏教版4年级英语"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"4年级数学": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "4年级数学"},
{"n": "沪教版","v": "沪教版4年级数学"},
{"n": "人教版","v": "人教版4年级数学"},
{"n": "北师大版","v": "北师大版4年级数学"},
{"n": "苏教版","v": "苏教版4年级数学"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"5年级语文": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "5年级语文"},
{"n": "沪教版","v": "沪教版5年级语文"},
{"n": "人教版","v": "人教版5年级语文"},
{"n": "北师大版","v": "北师大版5年级语文"},
{"n": "苏教版","v": "苏教版5年级语文"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"5年级英语": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "5年级英语"},
{"n": "沪教版","v": "沪教版5年级英语"},
{"n": "人教版","v": "人教版5年级英语"},
{"n": "北师大版","v": "北师大版5年级英语"},
{"n": "苏教版","v": "苏教版5年级英语"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"5年级数学": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "5年级数学"},
{"n": "沪教版","v": "沪教版5年级数学"},
{"n": "人教版","v": "人教版5年级数学"},
{"n": "北师大版","v": "北师大版5年级数学"},
{"n": "苏教版","v": "苏教版5年级数学"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"6年级语文": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "6年级语文"},
{"n": "沪教版","v": "沪教版6年级语文"},
{"n": "人教版","v": "人教版6年级语文"},
{"n": "北师大版","v": "北师大版6年级语文"},
{"n": "苏教版","v": "苏教版6年级语文"}]},

{"key": "duration","name": "时长","value": 
[{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"6年级英语": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "6年级英语"},
{"n": "沪教版","v": "沪教版6年级英语"},
{"n": "人教版","v": "人教版6年级英语"},
{"n": "北师大版","v": "北师大版6年级英语"},
{"n": "苏教版","v": "苏教版6年级英语"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}],

"6年级数学": [
{"key": "tid","name": "分类","value": [
{"n": "全部","v": "6年级数学"},
{"n": "沪教版","v": "沪教版6年级数学"},
{"n": "人教版","v": "人教版6年级数学"},
{"n": "北师大版","v": "北师大版6年级数学"},
{"n": "苏教版","v": "苏教版6年级数学"}]},

{"key": "duration","name": "时长","value": [
{"n": "全部","v": "0"},
{"n": "60分钟以上","v": "4"},
{"n": "30~60分钟","v": "3"},
{"n": "10~30分钟","v": "2"},
{"n": "10分钟以下","v": "1"}]}]
    },
    
    detailUrl:'/x/web-interface/view?aid=fyid',//二级详情拼接链接(json格式用)
    searchUrl:'/x/web-interface/search/type?search_type=video&keyword=**&page=1',
    searchable:2,
    quickSearch:0,
    headers:{
        "User-Agent":"PC_UA",
        "Referer": "https://www.bilibili.com",
        //"Cookie":"$bili_cookie"
        "Cookie":"DedeUserID=690781341;DedeUserID__ckMd5=cabc96906269c5b6;SESSDATA=2245ba24%2C1684212125%2C466fd%2Ab2;bili_jct=de6fdb60c10f8a83910aa55d79407b4e;"
    },
    timeout:5000,
    limit:8,
    play_parse:true,
    lazy:"js:let ids=input.split('_');let result={};let iurl='https://api.bilibili.com:443/x/player/playurl?avid='+ids[0]+'&cid='+ids[1]+'&qn=116';let html=request(iurl);let jRoot=JSON.parse(html);let jo=jRoot['data'];let ja=jo['durl'];let maxSize=-1;let position=-1;ja.forEach(function(tmpJo,i){if(maxSize<Number(tmpJo['size'])){maxSize=Number(tmpJo['size']);position=i}});let purl='';if(ja.length>0){if(position===-1){position=0}purl=ja[position]['url']}result['parse']=0;result['playUrl']='';result['url']=unescape(purl);result['header']={Referer:'https://live.bilibili.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'};result['contentType']='video/x-flv';input=result",
    double:false,
    推荐:'*',
    // 一级:'js:let html=request(input);let msg=JSON.parse(html).message;function title_rep(title){if(/keyword/.test(title)){title=title.replace(\'<em class="keyword">\',"").replace("</em>","").replace("&quot;","\'");log("名称替换👉"+title)};return title}if(msg!=="0"){VODS=[{vod_name:KEY+"➢"+msg,vod_id:"no_data",vod_remarks:"别点,缺少bili_cookie",vod_pic:"https://ghproxy.com/https://raw.githubusercontent.com/hjdhnx/dr_py/main/404.jpg"}]}else{let videos=[];let vodList=JSON.parse(html).data.result;vodList.forEach(function(vod){let aid=vod["aid"];let title=vod["title"].trim();title=title_rep(title);title=title_rep(title);title=title_rep(title);title=title_rep(title);let img="https:"+vod["pic"];let remark=vod["duration"];videos.push({vod_id:aid,vod_name:title,vod_pic:img,vod_remarks:remark})});VODS=videos}',
    一级:'js:let html=request(input);function title_rep(title){if(/keyword/.test(title)){title=title.replace(\'<em class="keyword">\',"").replace("</em>","");log("名称替换👉"+title)};return title}function turnDHM(duration){let min=duration.split(":")[0];let sec=duration.split(":")[1];if(min==0){return sec+"秒"}else if(0<min&&min<60){return min+"分"}else if(60<=min&&min<1440){if(min%60==0){let h=min/60;return h+"小时"}else{let h=min/60;h=(h+"").split(".")[0];let m=min%60;return h+"小时"+m+"分"}}else if(min>=1440){let d=min/60/24;d=(d+"").split(".")[0];let h=min/60%24;h=(h+"").split(".")[0];let m=min%60;let dhm="";if(d>0){dhm=d+"天"}if(h>=1){dhm=dhm+h+"小时"}if(m>0){dhm=dhm+m+"分"}return dhm}return null}let videos=[];let vodList=JSON.parse(html).data.result;vodList.forEach(function(vod){let aid=vod["aid"];let title=vod["title"].trim().replace("&quot;","\'");title=title_rep(title);title=title_rep(title);title=title_rep(title);let img="https:"+vod["pic"];let remark=turnDHM(vod["duration"]);videos.push({vod_id:aid,vod_name:title,vod_pic:img,vod_remarks:remark})});VODS=videos',
    二级:'js:let html=request(input);let jo=JSON.parse(html).data;let aid=jo["aid"];let title=jo["title"].replace(\'<em class="keyword">\',"").replace("</em>","");let pic=jo["pic"];let desc=jo["desc"];let year=jo["pubdate"];let dire=jo["owner"]["name"];let typeName=jo["tname"];let remark=jo["duration"];let vod={vod_id:aid,vod_name:title,vod_pic:pic,type_name:typeName,vod_year:year,vod_area:"bilidanmu",vod_remarks:remark,vod_tags:"mv",vod_director:dire,vod_content:desc};let ja=jo["pages"];let playurls=[];ja.forEach(function(tmpJo){let cid=tmpJo["cid"];let part=tmpJo["part"].replace("#","﹟").replace("$","﹩");playurls.push(part+"$"+aid+"_"+cid)});let playUrl=playurls.join("#");vod["vod_play_from"]="B站";vod["vod_play_url"]=playUrl;VOD=vod;',
    搜索:'*',
    预处理:'if(rule_fetch_params.headers.Cookie.startsWith("http")){rule_fetch_params.headers.Cookie=fetch(rule_fetch_params.headers.Cookie);setItem(RULE_CK,cookie)};log(rule_fetch_params.headers.Cookie)',
}