#!/usr/bin/env bash
set -euo pipefail

ACTION=${1:-noop}
DEFAULT_BASE=/workspace
if [ -w /workspace ] || [ ! -e /workspace ]; then
  BASE=$DEFAULT_BASE
else
  BASE=$(pwd)
  echo "[dev-start] /workspace not writable; using $BASE" >&2
fi
VENVDIR=$BASE/.venv
HACONF=$BASE/ha_config
BROKER_LOG=$HACONF/broker.out
HA_LOG=$HACONF/hass.out
DATASET=$BASE/testing/datasets/min_6000xh_tl.json
PIDDIR=$BASE/.pids
HA_PID_FILE=$PIDDIR/ha.pid
BROKER_PID_FILE=$PIDDIR/broker.pid

mkdir -p "$HACONF" "$PIDDIR" 2>/dev/null || true

activate() {
  if [ ! -f "$VENVDIR/bin/activate" ]; then
    echo "[dev-start] Creating virtualenv at $VENVDIR";
    python -m venv "$VENVDIR";
    . "$VENVDIR/bin/activate";
    pip install --upgrade pip >/dev/null 2>&1 || true
    if [ -f /workspace/requirements_dev.txt ]; then
      pip install -r /workspace/requirements_dev.txt >/dev/null 2>&1 || true
    fi
    pip install -e /workspace/external/growatt-rtu-broker >/dev/null 2>&1 || true
  else
    . "$VENVDIR/bin/activate"
  fi
}

is_running() { local f=$1; [ -f "$f" ] && kill -0 "$(cat "$f" 2>/dev/null)" 2>/dev/null; }

start_ha() {
  if is_running "$HA_PID_FILE"; then
    echo "[dev-start] HA already running (PID $(cat "$HA_PID_FILE"))"; return 0; fi
  activate
  echo "[dev-start] Starting Home Assistant..." | tee -a "$HA_LOG"
  nohup hass -c "$HACONF" >>"$HA_LOG" 2>&1 & echo $! > "$HA_PID_FILE"
  sleep 2
  if is_running "$HA_PID_FILE"; then echo "[dev-start] HA started PID $(cat "$HA_PID_FILE")"; else echo "[dev-start] HA failed (see $HA_LOG)"; fi
}

start_broker() {
  if is_running "$BROKER_PID_FILE"; then
    echo "[dev-start] Broker already running (PID $(cat "$BROKER_PID_FILE"))"; return 0; fi
  if [ ! -f "$DATASET" ]; then
    echo "[dev-start] Dataset missing: $DATASET" | tee -a "$BROKER_LOG"; return 1; fi
  activate
  echo "[dev-start] Starting broker (dataset mode)..." | tee -a "$BROKER_LOG"
  nohup growatt-broker run --mode dataset --dataset "$DATASET" --duration -1 >>"$BROKER_LOG" 2>&1 & echo $! > "$BROKER_PID_FILE"
  sleep 1
  if is_running "$BROKER_PID_FILE"; then echo "[dev-start] Broker started PID $(cat "$BROKER_PID_FILE")"; else echo "[dev-start] Broker failed (see $BROKER_LOG)"; fi
}

stop_proc() { local name=$1 pidfile=$2; if is_running "$pidfile"; then kill "$(cat "$pidfile")" 2>/dev/null || true; sleep 1; if is_running "$pidfile"; then kill -9 "$(cat "$pidfile")" 2>/dev/null || true; fi; rm -f "$pidfile"; echo "[dev-start] Stopped $name"; else echo "[dev-start] $name not running"; fi }

status() {
  if is_running "$HA_PID_FILE"; then echo "HA: RUNNING (PID $(cat "$HA_PID_FILE"))"; else echo "HA: stopped"; fi
  if is_running "$BROKER_PID_FILE"; then echo "Broker: RUNNING (PID $(cat "$BROKER_PID_FILE"))"; else echo "Broker: stopped"; fi
  echo "Logs: tail -f $HA_LOG | $BROKER_LOG"
}

case "$ACTION" in
  noop)
    echo "[dev-start] No action (explicit start required). Available: start|stop|restart|status|logs";
    ;;
  start)
    start_ha
    start_broker
    status
    ;;
  stop)
    stop_proc HA "$HA_PID_FILE"
    stop_proc Broker "$BROKER_PID_FILE"
    ;;
  restart)
    "$0" stop || true
    "$0" start
    ;;
  status)
    status
    ;;
  logs)
    echo "--- Home Assistant (last 40) ---"; tail -n 40 "$HA_LOG" || true
    echo "--- Broker (last 40) ---"; tail -n 40 "$BROKER_LOG" || true
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|logs}"; exit 2;
esac

exit 0
