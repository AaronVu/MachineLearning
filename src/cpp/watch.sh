# 函数: CheckProcess
# 功能: 检查一个进程是否存在
# 参数: $1 --- 要检查的进程名称
# 返回: 如果存在返回0, 否则返回1.
#------------------------------------------------------------------------------
CheckProcess()
{
  # 检查输入的参数是否有效
  if [ "$1" = "" ];
  then
    return 1
  fi

  #$PROCESS_NUM获取指定进程名的数目，为1返回0，表示正常，不为1返回1，表示有错误，需要重新启动
  PROCESS_NUM=`ps -ef | grep "$1" | grep -v "grep" | wc -l`
  if [ $PROCESS_NUM -eq 1 ];
  then
    return 0
  else
    return 1
  fi
}


# 检查test实例是否已经存在
while [ 1 ] ; do
 CheckProcess "test"
 CheckQQ_RET=$?
 if [ $CheckQQ_RET -eq 1 ];
 then

# 杀死所有test进程，可换任意你需要执行的操作

  killall -9 test
  exec ./test &
 fi
 sleep 1
done