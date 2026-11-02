cd /home/claude/mm; T="templates/Resources Code Template.html"; R=/home/claude/res80
echo "=== 8.4 $(date +%T)"; bash tools/v8/send_gate_nolive.sh $R/b84/b11/gate/websites.zip tools/v8 "$T" "src/8.4/8.4 Websites.docx" live/resources/index.html /websites/ $R/b84/b11/checks/full.txt NONE $R/b84/b11/send > $R/b84/b11/gate.txt 2>&1; tail -1 $R/b84/b11/gate.txt
echo "=== 8.0 $(date +%T)"; bash tools/v8/send_gate.sh $R/b80/n6/gate/resources.zip tools/v8 "$T" live/resources/index.html $R/b80/n6/checks/full.txt NONE $R/b80/n6/send > $R/b80/n6/gate.txt 2>&1; tail -1 $R/b80/n6/gate.txt
echo "=== 8.1 $(date +%T)"; bash tools/v8/send_gate.sh $R/b81x/n7/gate/books-by-montessori.zip tools/v8 "$T" live/books-by-montessori/index.html $R/b81x/n7/checks/full.txt NONE $R/b81x/n7/send > $R/b81x/n7/gate.txt 2>&1; tail -1 $R/b81x/n7/gate.txt
echo "=== 8.3 checks $(date +%T)"; cd $R/b83/b19; TZ=Asia/Shanghai date +%H:%M:%S > all.log; bash all.sh >> all.log 2>&1; TZ=Asia/Shanghai date +%H:%M:%S >> all.log; grep -i "result\|exit" checks/SUMMARY.txt | head
echo "=== done $(date +%T)"
