# get_J2L_images
某网站（J2L）的通用批量图片下载脚本

# 依赖
- python 2.7或3.5（低版本未经测试）
- requests 2.10.0（可以通过`pip install requests`安装）
- 请自备梯子

# 使用说明
- 确保python和requests已经安装好
- 确保梯子可以爬出墙外
- 运行`python get_images.py title [start] [stop] [outtime]`  
  - title: 神秘代码，此参数不可缺少
  - start: 下载图片的起始id，默认是`1`
  - stop: 下载图片的终止id，默认是`start + 10`
  - outtime: 失败N次后退出，默认是`10`
  
# 添加了命令模式 
- 运行`python get_images.py command [first_page] [last_page]` 
    - command: `-b`, `-m`, `-ne`, `-nr`四种类别的封面图
        1. -b: best rated
        2. -m: most wanted
        3. -ne: new entries
        4. -nr: new release
    - first_page: 下载的第一页的所有封面图，默认值是`1`
    - last_page: 下载的最后一页的所有封面图，默认和`first_page`一样
 

