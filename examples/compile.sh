cd /host/git/inria_wbc/
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/home/pal/install -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=/home/pal/install
make -j40
