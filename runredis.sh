#! /bin/sh
#
# runredis.sh
# Copyright (C) 2018 [Anselmos](github.com/anselmos) <anselmos@users.noreply.github.com>
#
# Distributed under terms of the MIT license.
#


docker rm -f pelican-redis
docker run --name pelican-redis -p 6379:6379 -v $(pwd)/redis:/data -d redis redis-server --appendonly yes
