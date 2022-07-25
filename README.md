# 基于Python的微博超话签到脚本

> 更新：支持青龙面板，前往[nodejs分支](https://github.com/Hellager/weibo_supertopic_sign/tree/nodejs)查看教程 

> 重要！：微博国际版升级为轻享版后无法抓包获取相关请求，请使用低版本进行抓包

## 项目简介
1. 基于Python实现微博超话关注列表的获取及签到
2. 根据签到结果选择不同渠道进行通知(钉钉, 微信, QQ)
3. 可通过腾讯云或阿里云实现每日定期签到

## 文件结构
weibo_supertopic_sign/ <br>
| -- notify/ <br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- \_\_init\_\_.py <br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- dingdingbot.py -> 钉钉机器人通知(钉钉) <br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- notifier.py    -> 全通知渠道运行 <br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- qmsgchan.py    -> Qmsg酱通知(QQ) <br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- serverchan.py  -> Server酱通知(微信) <br>
| -- \_\_init\_\_.py <br>
| -- config.json -> 本地参数json文件<br>
| -- config.py -> 从环境或本地获取参数<br>
| -- index.py -> 脚本入口文件<br>
| -- requirements.txt -> 安装依赖时所用文本<br>
| -- supertopicsign.py -> 微博超话关注列表的获取及签到<br>
| -- utils.py -> 系统打印设置<br>

## 抓包说明
  * 打开 **微博国际版** -> **关注的超话** -> **超话社区**
  * 开始抓包 -> 超话社区界面下拉刷新 -> 停止抓包
  * 在 **会话记录** 中 搜索 **cardlist** 点进去即可得到 ROW_URL 参数
[![IUVcLT.png](https://z3.ax1x.com/2021/11/10/IUVcLT.png)](https://imgtu.com/i/IUVcLT)

## 参数说明
|变量名称|变量含义  |
|--|--|
|ROW_URL(必需)| 微博国际版手机端抓包得到的原始链接<br>需包含**aid**, **gsid**, **from**, **s** |
|SIGN_TYPE(必需)| 签到方式选择 <br>DEFAULT -> 默认全部签到 <br>ONLY -> 仅签到在SIGN_LIST中的值 <br>EXCEPT -> 仅签到不在SIGN_LIST的值 |
|SIGN_LIST(可选)| 签到列表设置，直接输入超话名称，以 ; 间隔 |
|DING_SECRET(可选)| 钉钉机器人密钥 |
|DING_WEBHOOK(可选)| 钉钉机器人webhook |
|SERVER_KEY(可选)| Server酱 Key |
|QMSG_KEY(可选)| Qmsg酱 Key |
|IS_SORT(可选)| 结果是否根据等级排序<br>INCREASE -> 按等级升序 <br>DECREASE -> 按等级降序|
|DISP_TYPE(必需)| 结果是否展示等级信息 <br>DEFAULT -> 默认成功简略显示 <br>DETAIL-> 成功签到显示等级 |

## 更新说明
2022-2-24 添加测试程序 方便调试纠错 <br>
&nbsp;&nbsp;&nbsp;&nbsp; 测试前填写好 test/config.json 中参数 直接运行test/test_index.py 即可
&nbsp;&nbsp;&nbsp;&nbsp; 结果可在 test/data 文件夹中查看 均以 json 文件形式保存

## 使用说明
1. 本地使用 <br>
    下载代码至本地 要求环境 Python 3.6.8 及以上 <br>
    填写好目录中 config.json 中的参数 <br>
    打开命令行 运行如下命令
    ```Python
    pip install -r requirements.txt
    python index.py
    ```
2. 腾讯云函数运行 <br>
    * 登录 **腾讯云**， 打开右上角 **控制台**， 找到 **我的资源** -> **云函数**，点击打开, 找到 **函数服务** -> **新建**， 选择 **自定义创建**， 设置 **函数名称**， 选择 **本地上传ZIP包**， 上传 [supertopic_sign_V1.0.3](https://pan.baidu.com/s/1g6uzlpHtP45C8W42_8ivrQ) 提取码 70ef，点击完成，完成新建云函数 <br>
    * 进入 **函数管理** -> **函数配置** -> 设置**执行超时时间** -> 设置**环境变量** <br>
    * 进入 **触发管理** -> **创建触发器** -> 选择 **自定义触发周期** -> 设置**corn表达式** -> **提交** 即完成设置


## 注意事项
为避免过快请求触发检测机制 程序中相关延时设置较为保守 若发现云端执行时程序无法签到所有超话 可尝试以下方法 <br>
1. 修改代码段中延时时间
```Python
//supertopicsign.py 68行
time.sleep(random.randint(5, 10))
//supertopicsign.py 154行
time.sleep(random.randint(15, 30))
```
2. 使用 SIGN_TYPE 和 SIGN_LIST 参数对超话进行分批次签到 <br>

## 注意事项2
目前发现存在微博账号 其数据返回结构体与一般账号存在差异 会导致无法正确获取相关参数<br>
如果发现自己的账号存在这种情况且不知道怎么解决 请在ISSUE中提出并贴出数据的返回结构<br>
我会尽力解决并更新程序
