#appengine
=========
appengine 修改自雨痕的项目：[appengine](https://github.com/qyuhen/appengine)

**修改内容**

* 修改装载配置方式(b0d816a)
* 增加config配置项
* * 可选使用pdb
* * 可选支持django
* 改变django callback，支持appengine调度器(dce1866)
* 让pdb进入更准确的异常现场(fb8ca0b)
* 可安装到系统环境 编写setup.py
* 修复原项目某些情况下，debug模式无法重新载入模块bug.(0f9597d)

**TODO**

* 性能测试


#安装说明
===================
##linux
首先下载源码，可以直接点击download下载，[点击下载](https://github.com/windprog/appengine/archive/master.zip)，也可以在shell下输入:

	git clone https://github.com/windprog/appengine.git

进去后可以看到setup.py这个就是安装文件了，运行安装到python系统环境:

	python setup.py install

也可直接将 httpappengine 文件夹复制到项目目录使用


#演示
===================
#运行demo, config.py可修改参数。

    python run.py