python3 stateful_counter.py > ./artifacts/stateful_counter.teal
python3 clear_program.py > ./artifacts/clear_program.teal

./sandbox copyTo ./artifacts/stateful_counter.teal
./sandbox copyTo ./artifacts/clear_program.teal



