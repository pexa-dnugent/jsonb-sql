#!/usr/bin/env bash
case "$1" in
  start)
    docker compose --profile db up -d
    ;;
  stop)
    docker compose --profile db down
    ;;
  *)
    echo "Usage: $0 [start|stop]"
    ;;
esac
