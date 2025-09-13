#!/usr/bin/env bash
set -euo pipefail

# Autostart script for growatt broker inside devcontainer.
# Idempotent: will not start a second copy if one is already listening on the TCP port.

VENVDIR=""
LOGDIR=/workspace/ha_config
LOGFILE="$LOGDIR/broker.out"
PORT=${GROWATT_BROKER_PORT:-5020}
DATASET=${GROWATT_DATASET:-/workspace/testing/datasets/min_6000xh_tl.json}

mkdir -p "$LOGDIR"

if ! lsof -i TCP:"$PORT" -sTCP:LISTEN -Fp >/dev/null 2>&1; then
  echo "[start-broker] Starting broker on port $PORT ..." | tee -a "$LOGFILE"
  # shellcheck disable=SC1091
  # Use dataset mode (simulator) by default; allow override via env var GROWATT_BROKER_MODE
  MODE=${GROWATT_BROKER_MODE:-dataset}
  # Allow selecting CLI (prototype vs bus) via GROWATT_BROKER_CLI (growatt-broker|growatt-broker-bus)
  # Default to prototype CLI (dataset mode) for dev container unless overridden
  CLI=${GROWATT_BROKER_CLI:-growatt-broker}

  # If bus CLI selected but required serial devs not present, fall back to prototype
  if [ "$CLI" = "growatt-broker-bus" ]; then
    : "${GROWATT_INV_DEV:=/dev/ttyINV0}"
    : "${GROWATT_SHINE_DEV:=/dev/ttySHINE0}"
    if [ ! -e "$GROWATT_INV_DEV" ] || [ ! -e "$GROWATT_SHINE_DEV" ]; then
      echo "[start-broker] Serial devices missing ($GROWATT_INV_DEV / $GROWATT_SHINE_DEV). Falling back to dataset prototype." | tee -a "$LOGFILE"
      CLI=growatt-broker
    fi
  fi
  set -x
  # If using bus CLI we can pass --tcp; prototype CLI lacks this arg
  if [ "$CLI" = "growatt-broker-bus" ]; then
    nohup "$CLI" --inverter "$GROWATT_INV_DEV" --shine "$GROWATT_SHINE_DEV" --tcp 0.0.0.0:"$PORT" >>"$LOGFILE" 2>&1 &
  else
    # Ensure dataset exists
    if [ ! -f "$DATASET" ]; then
      echo "[start-broker] Dataset not found: $DATASET" | tee -a "$LOGFILE"
      exit 0
    fi
    nohup "$CLI" run --mode dataset --dataset "$DATASET" --duration -1 >>"$LOGFILE" 2>&1 &
  fi
  PID=$!
  set +x
  echo "[start-broker] Started (PID $PID)" | tee -a "$LOGFILE"
else
  echo "[start-broker] Broker already listening on $PORT; skipping start." | tee -a "$LOGFILE"
fi

exit 0
