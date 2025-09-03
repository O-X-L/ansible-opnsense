#!/bin/bash

if [ -z "$1" ]
then
  DEST_DIR='build'
else
  DEST_DIR="$1"
fi

set -euo pipefail

function log() {
  msg="$1"
  echo ''
  echo "### ${msg} ###"
  echo ''
}

cd "$(dirname "$0")"

SRC_DIR="$(pwd)"

TS="$(date +%s)"
TMP_DIR="/tmp/${TS}"
mkdir -p "${TMP_DIR}"

VENV_BIN='/tmp/.ag-docs-venv/bin/activate'

if [ -f "$VENV_BIN" ]
then
  source "$VENV_BIN"
fi

log 'BUILDING DOCS'
export PYTHONWARNINGS='ignore'
sphinx-build -b html source/ "${TMP_DIR}/" >/dev/null

log 'PATCHING METADATA'
cp "${SRC_DIR}/meta/"* "${TMP_DIR}/"

HTML_META_SRC="<meta charset=\"utf-8\" />"
HTML_META="${HTML_META_SRC}<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; img-src 'self' https://files.oxl.at; style-src 'self' https://files.oxl.at 'unsafe-inline'; script-src 'self' https://files.oxl.at 'unsafe-inline' 'unsafe-eval'; connect-src 'self';\">"
HTML_META="${HTML_META}<link rel=\"icon\" type=\"image/webp\" href=\"https://files.oxl.at/img/oxl3_sm.webp\">"
HTML_META_EN="${HTML_META}"  # <link rel=\"alternate\" href=\"https://docs.o-x-l.at\" hreflang=\"de\">
# HTML_LOGO_LINK_SRC='href=".*Go to homepage"'
# HTML_LOGO_LINK_EN='href="https://www.o-x-l.com" class="oxl-nav-logo" title="OXL IT Services Website"'
HTML_LANG_NONE='<html'
HTML_LANG_EN='html lang="en"'

cd "${TMP_DIR}/"

sed -i "s|$HTML_META_SRC|$HTML_META_EN|g" *.html
sed -i "s|$HTML_META_SRC|$HTML_META_EN|g" */*.html
# sed -i "s|$HTML_LOGO_LINK_SRC|$HTML_LOGO_LINK_EN|g" *.html
# sed -i "s|$HTML_LOGO_LINK_SRC|$HTML_LOGO_LINK_EN|g" */*.html
sed -i "s|$HTML_LANG_NONE|<$HTML_LANG_EN|g" *.html
sed -i "s|$HTML_LANG_NONE|<$HTML_LANG_EN|g" */*.html

log 'ACTIVATING'
cd "$SRC_DIR"
if [ -d "$DEST_DIR" ]
then
  rm -r "$DEST_DIR"
fi
mkdir -p "${DEST_DIR}/"

mv "${TMP_DIR}/"* "${DEST_DIR}/"

touch "${DEST_DIR}/${TS}"

rm -rf "$TMP_DIR"

log 'FINISHED'
