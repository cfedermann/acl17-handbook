#!/bin/bash
for file in $(ls data); do
  num=$(cat data/$file/proceedings/order | ./scripts/verify_schedule.py > /dev/null 2>&1; echo $?)
  if test $num -ne 0; then
    echo -e "$file\t$num"
  fi
done
