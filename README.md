<!--
 * @Author: Hellager
 * @Date: 2022-06-23 11:27:24
 * @LastEditTime: 2022-06-23 16:52:37
 * @LastEditors: Hellager
-->
## 使用说明

### 本地运行

1. 安装相关依赖

```shell
npm i axios dayjs dotenv qs
```

2. 添加环境变量

   通知相关变量具体可参考 SendNotify.js 中参数

```shell
touch .env
echo BARK_PUSH="xxx" > ./.env
echo COOKIE_WEIBO="xxxx" > ./.env
```

3. 运行脚本

```shell
node ./Sign_Weibo.js
```

### 青龙面板运行

1. 安装相关依赖

   选择 **依赖管理** -> NodeJs, 选择右上角 **新建依赖**, 依次添加 **axios dayjs dotenv qs** 即可

2. 添加脚本

   选择 **脚本管理**, 点击右上角 **+ 按钮**, 类型 **空文件**, 文件名自定义即可，暂定为 **Sign_Weibo.js**, 注意后缀必须添加。点击确定完成新建。

3. 添加代码

   点击左侧 Sign_Weibo.js, 点击右上角编辑按钮，将仓库中的 Sign_Weibo.js 文件中的内容**全部复制**过去，然后点击保存

4. 添加相关环境变量
   点击 **环境变量**, 点击 **新建变量**，名称**COOKIE_WEIBO**, 自动拆分选 **否**, 值填抓包获取到的值，多个 COOKIE 请用 **';'** 隔开,通知相关变量参考 SendNotify.js 中参数

5. 添加定时任务
   点击 **定时任务**， 点击右上角新建任务，名称自定义即可，输入命令
   
   ```shell
    task Sign_Weibo.js
   ```

   设置自己想要的定时，点击确定保存

6. 测试是否成功

   在任务操作一栏，直接点击运行按钮，然后查看日志


