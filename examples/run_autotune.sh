export LD_LIBRARY_PATH=/host/git/install/lib:/home/pal/install/lib:/usr/local/nvidia/lib:/usr/local/nvidia/lib64
export PATH=/host/git/install:/home/pal/install:/home/pal/bin:/usr/local/nvidia/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /host/git/talos_autotune/
ldd build/*
./build/talos_urdf_params
