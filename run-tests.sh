#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2015-2020 CERN.
# SPDX-License-Identifier: MIT

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Always bring down docker services
function cleanup {
    eval "$(docker-services-cli down --env)"
}
trap cleanup EXIT

eval "$(docker-services-cli up --mq ${CACHE:-redis} --env)"
python -m pytest $@
