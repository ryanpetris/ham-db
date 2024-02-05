#!/bin/bash

set -e
set -o pipefail

curl -fL -o 'l_amat.zip' 'https://data.fcc.gov/download/pub/uls/complete/l_amat.zip'
exec ./hamdb-import.sh l_amat.zip