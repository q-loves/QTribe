# QTribe（钦部落）Django+Vue实现的博客平台
## 项目介绍<br>
### 钦部落  这是一个博客平台，用户注册自己的账号后可在平台上 `发布文章`（休闲，学术，生活，科技类皆可），也可自己`创作视频`上传，也可以`分享生活细节`（文案，照片 等）。我下面描述的内容是已经实现的功能，还有好多功能还正在更新。大家可以fork下来和我一起完成，非常欢迎呦！！！:blush:<br>
______
### 技术要点：<br>
### 1.基于Django+Vue实现平台功能，采用前后端不分离的模式。<br>
### 2.QQ，微信等第三方登录。<br>
### 3.配置redis储存临时动态信息，提升用户访问效率，减小mysql压力。<br>
### 4.视频，照片等静态文件采用分布式储存，fastdfs（部署在docker上）。
### 5.elasticsearch+haystack搜索引擎（部署在docker上）。
______
### 注：现在项目还未做完，大家如果想一起做的话，可以先fork到自己本地。:sparkling_heart:<br>
### 1.先在自己电脑的C:\Windows\System32\drivers\etc\hosts文件里面映射一下地址（如下图）<br>
### 2.在pycharm（其他编译器也可，我习惯用这个）里面配置一下环境pip install requirements.txt。<br>
### 3.创建自己的mysql数据库，把setting.dev里面mysql的配置改成自己的。配置好后，运行python manage.py makemigrations 和 python manage.py migrate 命令进行数据库迁移。
### 3.下载docker，在docker上拉取elasticsearch镜像，创建elasticsearch容器并开启。（这一步是实现搜索功能的，如果不按照步骤来，会报错:confused:）<br>
### 4.运行命令python manage.py runserver 8083（注意，必须是8083端口）可启动项目.<br>
![HE(D~H6PGZW55OQ`G%~BG`I(1)_edit_400445283161146](https://github.com/q-loves/QTribe/assets/121675743/d96099a0-9e63-4836-b0fb-92a737ae522f)


## 项目具体实现<br>
____
### 1.用户注册账号 <br>
_____
![image](https://github.com/q-loves/QTribe/assets/121675743/27b80162-2f77-4485-975b-ecfb336827e4) 
### 用户注册完后即可进入平台<br>
### 2.用户登录:当用户已有平台账户时，可点击右侧sign in按钮进入登录页面
---
![image](https://github.com/q-loves/QTribe/assets/121675743/84f6d42b-39b5-49dc-815c-f972601bbd33)
### (1)可采用用户名，密码登录方式。(2)可采用第三方登录，QQ，微信等。例如QQ登陆，如果用户未绑定QQ号，那么扫码后会自动跳到绑定用户页面
---
![image](https://github.com/q-loves/QTribe/assets/121675743/1a9f32bd-8130-4033-8f99-8f0f601b0844)
### 绑定后就可以进入平台中心。下次再用QQ登陆时，扫码后就可直接进入平台中心。
____
![image](https://github.com/q-loves/QTribe/assets/121675743/a0aa5c91-ba46-4a0a-8413-269312a0f7c1)

## 平台内部结构
---
### 可以在看点广场里面浏览平台用户们上传的各种作品，自己可以点赞收藏，评论等
---
![image](https://github.com/q-loves/QTribe/assets/121675743/1e55a82a-3959-473e-bd79-23ca348cc90d)
![image](https://github.com/q-loves/QTribe/assets/121675743/a88131f3-f556-44c8-9844-9540e91407ef)
### 在个人中心可查看自己信息 自己的作品 点赞列表 收藏列表等
---
![image](https://github.com/q-loves/QTribe/assets/121675743/0d314a41-401c-424e-aab0-ed4ffb23439f)
---
### 在右上角的修改身份卡里面可以修改自己的个人信息
---
![image](https://github.com/q-loves/QTribe/assets/121675743/ded635b1-cae3-48ea-aae7-e16609e8bd24)
### 自己可以在动手创作模块里面，发布视频 上传文章 分享生活等。
---
![image](https://github.com/q-loves/QTribe/assets/121675743/9a835c0f-8dfe-488c-a9d4-797d7c63b044)




