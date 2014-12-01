#appengine
=========
appengine 修改自雨痕的项目：[appengine](https://github.com/qyuhen/appengine)

**修改内容**

* 修改装载配置方式
* 可配置兼容django, 且支持appengine调度器
* 让pdb更好的进入异常现场
* 增加config配置项，可选是否使用ipdb进行调试

**TODO**

* 查看django的session实现方式，现在的appengine会用多进程运行，如果是使用内存实现的话需要单进程或者更改实现方式（同用户使用相同worker）。
* 可安装到系统环境 编写setup.py

#安装说明
===================
##linux
首先下载源码，可以直接点击download下载，[点击下载](https://github.com/windprog/appengine/archive/master.zip)，也可以在shell下输入:

	git clone https://github.com/windprog/appengine.git

如果是压缩包记得解压，安装依赖包：

    sudo pip install -r requirements.txt

进去后可以看到setup.py这个就是安装文件了，注意你需要有python环境,运行安装到python系统环境:

	python setup.py

也可直接将 engine 复制到项目目录使用
