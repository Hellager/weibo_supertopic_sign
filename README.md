# 基于Python的微博超话签到脚本
## 项目简介
1. 基于Python实现微博超话关注列表的获取及签到
2. 根据签到结果选择不同渠道进行通知(钉钉, 微信, QQ)
3. 可通过Github Actions 实现云端定期执行

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

## 参数说明
|变量名称|变量含义  |
|--|--|
|ROW_URL(必需)| 抓包得到原始链接 需包含**aid**, **gsid**, **from**, **s** |
|SIGN_TYPE(必需)| 签到方式选择 <br>DEFAULT -> 默认全部签到 <br>ONLY -> 仅签到在SIGN_LIST中的值 <br>EXCEPT -> 仅签到不在SIGN_LIST的值 |
|SIGN_LIST(可选)| 签到列表设置，直接输入超话名称，以 ; 间隔 |
|DING_SECRET(可选)| 钉钉机器人密钥 |
|DING_WEBHOOK(可选)| 钉钉机器人webhook |
|SERVER_KEY(可选)| Server酱 Key |
|QMSG_KEY(可选)| Qmsg酱 Key |
|IS_SORT(可选)| 结果是否根据等级排序<br>INCREASE -> 按等级升序 <br>DECREASE -> 按等级降序|
|DISP_TYPE(必需)| 结果是否展示等级信息 <br>DEFAULT -> 默认成功简略显示 <br>DETAIL-> 成功签到显示等级 |

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
    * 登录 **腾讯云**， 打开右上角 **控制台**， 找到 **我的资源** -> **云函数**，点击打开, 找到 **函数服务** -> **新建**， 选择 **自定义创建**， 设置 **函数名称**， 选择 **本地上传ZIP包**， 上传 [supertopic_sign_V1.0](https://pan.baidu.com/s/1Pei34Zm0O7C5AHOCzCVNDw) 提取码 tgax，点击完成，完成新建云函数 <br>
    * 进入 **函数管理** -> **函数配置** -> 设置**执行超时时间** -> 设置**环境变量** <br>
    * 进入 **触发管理** -> **创建触发器** -> 选择 **自定义触发周期** -> 设置**corn表达式** -> **提交** 即完成设置

3. Github Actions运行<br>
    * fork本仓库 在 **.github/workflows** 文件夹下找到 **dailysign.yml**
    * 打开yml文件 修改第3~5行代码为如下即可每天定时九点运行
      ```Yml
      on: 
        schedule: 
          - cron: '0 9 * * *'
      ```
     * 找到仓库 **Settings** -> **Secrets** -> **New repository secret** 根据参数说明**添加变量及变量值** 即完成设置

