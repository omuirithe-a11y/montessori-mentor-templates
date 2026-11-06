#!/bin/bash
# 6 Nov 2026 (owner 10:53 "yes", lessons list item 6; lessons 42, 49, 65): every figure in a message to the owner is first
# written here by a command - name, the command's output, the command itself and the clock time - and the draft quotes only
# this file; the message checker is given it as the evidence list.  Usage: facts.sh <facts file> <name> <command...>
set -u; F=$1; N=$2; shift 2
OUT=$(bash -c "$*" 2>&1 | head -20)
{ echo "## $N  ($(date +%H:%M:%S))"; echo "command: $*"; echo "$OUT"; echo; } >> "$F"; echo "$N: $OUT"
