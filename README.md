# get_J2L_images
某网站（J2L）的通用批量图片下载脚本

# 依赖
- python 2.7或3.5（低版本未经测试）
- requests 2.10.0（可以通过`pip install requests`安装）
- 请自备梯子

# 使用说明
- 确保python和requests已经安装好
- 确保梯子可以爬出墙外
- 运行`python run.py code start stop`  
  - code: 神秘代码，此参数不可缺少
  - start: 下载图片的起始id，默认是`1`
  - stop: 下载图片的终止id，默认是`start + 10`
