#!/bin/bash
# 如果报错，说明没有相关包，就改用anaconda的python，或者装一下这些包
# 如果想停止程序，可以关掉命令行窗口，或者新开一个窗口，执行
# ps -ef | grep "python"
# 会有类型这种输出
#  501 17834 17769   0 10 418  ttys002    0:09.86 /Users/higgs/anaconda2/bin/python /Users/higgs/anaconda2/bin/ipython
#  501 95866 93508   0  6:15下午 ttys004    0:00.48 /usr/bin/python /usr/local/bin/ipython
#  501  5222  4592   0  1:16上午 ttys006    0:00.01 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn python
# 找到对应的进程号，如上面的5222，执行
# kill 5222
# 进程就停止了
python main.py --token_path='./tokens.txt' --api_path='./registered_api.txt' --software_path='./software.txt' 