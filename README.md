# caelus

## 开发环境

开发项目需要 python3, 建议 3.6 ,修改前端页面需要node和yarn环境，请自行安装

其中页面在 `page` 下

## 如何运行项目

1. 根据requirements.txt 安装相关依赖，可以运行 `install.sh` 进行安装
1. 相关依赖安装完成后，如果项目无 data.db 文件，请运行 init.py 生成，该文件为一个sqlite文件
1. 如果你已经安装好node, yarn, 并安装了对应node依赖，你可以运行`package_html.sh` 来生成页面
1. 启动，你可以python app.py 来启动项目, 默认端口是 5000, 如果你想修改默认端口，需要将前端页面中的端口号一并修改
1. 当然，你也可以用脚本启动，我已经帮你写好了




## Page

``` bash
# install dependencies
yarn

# serve with hot reload at localhost:8080
yarn run dev

# build for production with minification
yarn run build
```

> 最后，祝你幸福😒