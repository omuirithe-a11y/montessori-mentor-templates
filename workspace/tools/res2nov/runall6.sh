for d in b80/n7 b81x/n10 b83/b21; do (cd /home/claude/res80/$d; TZ=Asia/Shanghai date +%H:%M:%S > all.log; bash all.sh >> all.log 2>&1; TZ=Asia/Shanghai date +%H:%M:%S >> all.log); done
