#!/bin/bash

set -euo pipefail

# Set some defaults as documented
TIMEOUT=${TIMEOUT:-"3m"}

# Wait for the instance to become available
if [[ -v DATAVERSE_URL ]] && [[ -n "${DATAVERSE_URL}" ]]; then
  echo "Waiting for ${DATAVERSE_URL} to become ready in max ${TIMEOUT}."
  wait4x http "${DATAVERSE_URL}/api/info/version" -i 8s -t "$TIMEOUT" --expect-status-code 200 --expect-body-json data.version
fi

# base command
CMD="python /app/dataverse-cli.py $@"

# Check if DATAVERSE_URL environment variable is set to value
if [[ -v DATAVERSE_URL ]] && [[ -n "${DATAVERSE_URL}" ]]; then
    CMD+=" --dataverse-url="${DATAVERSE_URL}
fi
# Check if PREVIEWER_PROVIDER_URL environment variable is set to value
if [[ -v PREVIEWER_PROVIDER_URL ]] && [[ -n "${PREVIEWER_PROVIDER_URL}" ]]; then
    CMD+=" --provider-url="${PREVIEWER_PROVIDER_URL}
fi
# Check if INCLUDE_PREVIEWERS environment variable is set to value
if [[ -v INCLUDE_PREVIEWERS ]] && [[ -n "${INCLUDE_PREVIEWERS}" ]]; then
    CMD+=" --includes="${INCLUDE_PREVIEWERS}
fi
# Check if EXCLUDE_PREVIEWERS environment variable is set to value
if [[ -v EXCLUDE_PREVIEWERS ]] && [[ -n "${EXCLUDE_PREVIEWERS}" ]]; then
    CMD+=" --excludes="${EXCLUDE_PREVIEWERS}
fi
# Check if REMOVE_EXISTING environment variable is set to "true" (case insensitive)
if [[ -v REMOVE_EXISTING ]] && [[ "${REMOVE_EXISTING,,}" == "true" ]]; then
    CMD+=" --remove-existing"
fi
echo "$CMD"
# Run the command with any additional arguments passed to the entrypoint
$CMD