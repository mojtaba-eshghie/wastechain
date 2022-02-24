./sandbox goal account list # listing the accounts with balances
./sandbox goal account export --address address_from_list_above # to export nmemonic




# these are to deploy a teal application on blockchain:
python3 stateful_counter.py > ./artifacts/stateful_counter.teal
python3 clear_program.py > ./artifacts/clear_program.teal
# these try to copy the files to the sandbox container
./sandbox copyTo ./artifacts/stateful_counter.teal
./sandbox copyTo ./artifacts/clear_program.teal
# creating the application
./sandbox goal app create --creator QNWYDABSRUSNAMUEZPLWORIRWNHRHDYT677XR3V5LBY5BZPHULWMMP6TOI --global-byteslices 0 --global-ints 1 --local-byteslices 0 --local-ints 0 --approval-prog sc.teal --clear-prog cp.teal
# calling the app
./sandbox goal app call --from QNWYDABSRUSNAMUEZPLWORIRWNHRHDYT677XR3V5LBY5BZPHULWMMP6TOI --app-id 2
