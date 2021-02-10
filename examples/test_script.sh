cd /host/git/inria_wbc/
cd build
mkdir /host/data/$RESULT_DIR
FILE=/host/data/$RESULT_DIR/test_result_talos-`date +%m-%d-%H-%M-%S`-$RAND.dat
cd tests
./test_behaviors_talos $ARGS > $FILE