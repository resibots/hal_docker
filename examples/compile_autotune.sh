set -x
rm -rf /host/git/install/
export LD_LIBRARY_PATH=/host/git/install/lib:/home/pal/install/lib:/usr/local/nvidia/lib:/usr/local/nvidia/lib64
export PATH=/host/git/install:/home/pal/install:/home/pal/bin:/usr/local/nvidia/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /host/git/tsid/
rm -rf build
mkdir build
cd build
cmake -DBUILD_PYTHON_INTERFACE=OFF -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_PREFIX_PATH=/home/pal/install/ -DCMAKE_INSTALL_PREFIX=/host/git/install ..
make -j40
make install
cd /host/git/inria_wbc/
git checkout autotune_2021
rm -rf build
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_PREFIX_PATH=/host/git/install:/home/pal/install/ -DCMAKE_INSTALL_PREFIX=/host/git/install ..
make -j40
make install
cd /host/git/install/lib
ldd *
cd /host/git/talos_autotune
rm -rf build
./waf clean
./waf configure --sferes=/home/pal/sferes2  --tsid=/host/git/install --inria_wbc=/host/git/install  --robot_dart=/home/pal/install/   --prefix=/host/git/install  
./waf 
./waf install