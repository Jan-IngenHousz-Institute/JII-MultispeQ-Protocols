##
# Run build logic for documentation
##

echo "Build protocol overview document and separate documents for each protocol."
python3 docs/source/protocols.py

echo "Build protocol syntax based on schema.json file"
python3 docs/source/schema.py

cd docs

echo "Clean Build"
make clean

echo "Start new Build"
make html

cd ..