#!/usr/bin/env bash

rm -rf output
mkdir -p output/pbt
cp -r pbt output/pbt/
cp bin/pbt output/pbt/__main__.py
cd output/pbt
find -name ___pycache__ -exec rm -r {} \;
find -name \*.pyc -exec rm {} \;
zip -r pbt .
echo "#!/usr/bin/env python3" > header
cat header pbt.zip > pbt.bin
chmod u+x pbt.bin
mv pbt.bin ..
