#!/usr/bin/env bash

# 构建任务计划
base_path=$(cd `dirname $0`; pwd)
cron_content="20 12 * * * python ${base_path}/git_batch.py >/dev/null 2>&1"

echo cron_content >> $USER
