cd /host/git/inria_wbc/
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/home/user/install -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=/home/user/install
make -j40