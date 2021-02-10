# HAL::docker
Tool to run binaries in a docker image on the HAL cluster (OAR based)

## Examples
### Compile and run in the docker 
```
hal-docker.py --image registry.gitlab.inria.fr/locolearn/public/docker_inria_wbc/inria_wbc:latest  --compile examples/compile.sh  --script examples/test_script.sh --dir /nfs/hal01/jmouret
```

### Compile and submit with 6 replicates
```
hal-docker.py --image registry.gitlab.inria.fr/locolearn/public/docker_inria_wbc/inria_wbc:latest  --compile examples/compile.sh  --script examples/test_script.sh --dir /nfs/hal01/jmouret --submit --replicates 6
```


### Kill a job
Do not use oardel directly because it does not clean properly the docker containers!

```
hal-docker.py --kill  745342
```


## Help
```
usage: hal-docker.py [-h] [-c CMD] [-C COMPILE] [-d DIR] -i IMAGE [-k KILL]
                     [-n CORES] [-r REPLICATES] [-S SCRIPT] [-s] [-v]
                     [-w WALLTIME]

optional arguments:
  -h, --help            show this help message and exit
  -c CMD, --cmd CMD     command to run
  -C COMPILE, --compile COMPILE
                        compilation script
  -d DIR, --dir DIR     directory to be mounted as /host
  -i IMAGE, --image IMAGE
                        DOCKER image
  -k KILL, --kill KILL  kill a job [--kill job_number]
  -n CORES, --cores CORES
                        number of cores for OAR [use 24 for a full node, 32
                        for the 'fat nodes']
  -r REPLICATES, --replicates REPLICATES
                        number of replicates
  -S SCRIPT, --script SCRIPT
                        script to compile and run
  -s, --submit          submit the job to OAR
  -v, --verbose         print more information
  -w WALLTIME, --walltime WALLTIME
                        walltime for the OAR job (warning the job will be
                        killed after this time)
```
