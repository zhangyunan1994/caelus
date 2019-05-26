#!/usr/bin/env bash
cd page
yarn run build
cp dist/index.html ../templates
cp -r dist/static/ ../static
echo '恭喜你，你居然成功了'