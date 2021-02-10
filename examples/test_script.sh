cd /host/git/inria_wbc/
cd build
FILE=/host/data/test_result_talos-`date +%m-%d-%H-%M-%S`.dat
cd tests
./test_behaviors_talos > $FILE
