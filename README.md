# Books

#### 项目介绍
农业统计年鉴项目：基于Django开发的Web站点，将爬虫采集的统计年鉴信息通过该网站共享。

#### 使用说明

1. Media文件夹：采集的中国农业统计年鉴文件，包括CAJ、PDF、Excel三种文件类型。
2. conf文件夹：Ubuntu+Nginx+Uwsgi+Django,部署的配置文件，需要安装对应的软件。
1. data文件夹：数据源文件，需要将里面的数据导入数据库中，网站才能正常显示。
3. 相关依赖库：项目是从大项目抽取出来单独做的一个小项目，requirements.py文件中没有排除与本项目无关的库，请自行研究。
            `pip install -r requirements`
1. Settings配置：请将数据库等相关配置改成自己的配置信息。
