#!/usr/bin/python3
import argparse
import subprocess
import sys,os

# wrap a script in the docker environment and put it in output_script
# if no input script, uses args.cmd
def make_docker_script(args, input_script, output_script, verbose):
    # start (run) the docker image
    script = ''
    if (verbose):
        script += 'set -x\n'
    script += "DOCKER_ID=`docker run -t --user=user -w /home/user  --privileged=true -d -v {}:/host {} /bin/bash`\n".format(args.dir, args.image)

    if args.verbose:
        script += "docker ps\n"

    # this is so we can control-c/oardel a process and close the docker
    script += 'trap "echo stopping $DOCKER_ID with SIGINT; docker stop $DOCKER_ID; docker rm $DOCKER_ID;exit 1" SIGINT\n'
    script += 'trap "echo stopping $DOCKER_ID with SIGKILL; docker stop $DOCKER_ID; docker rm $DOCKER_ID;exit 1" SIGKILL\n'
    script += 'trap "echo stopping $DOCKER_ID with SIGTERM; docker stop $DOCKER_ID; docker rm $DOCKER_ID;exit 1" SIGTERM\n'
    script += 'trap "echo stopping $DOCKER_ID with SIGQUIT; docker stop $DOCKER_ID; docker rm $DOCKER_ID;exit 1" SIGQUIT\n'
    script += 'trap "echo stopping $DOCKER_ID with SIGABRT; docker stop $DOCKER_ID; docker rm $DOCKER_ID;exit 1" SIGABRT\n'
    script += 'trap "echo stopping $DOCKER_ID with SIGABRT; docker stop $DOCKER_ID; docker rm $DOCKER_ID;exit 1" SIGCHLD\n'

    script += 'trap\n'

    s = ''
    if verbose:
        s = 'set -x;'
    for l in open(input_script):
        s += l[0:-1] + ';'
    script += "docker exec $DOCKER_ID /bin/bash -c \'{}\' & \n".format(s)

    script += "CHILD=$!\n"
    script += "wait \"$CHILD\"\n"
    # stop and remove the docker image
    script += "docker stop $DOCKER_ID;\n"
    script += "docker rm $DOCKER_ID;\n"

    if args.verbose:
        print(script)
    with open(output_script, 'w') as f:
        f.write(script)

    return output_script


def run(cmd, verbose):
    if verbose:
        print ("CMD: " + cmd)
    subprocess.run(cmd, shell=True)

def parse_args():
    # setup arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--cmd", help="command to run", type=str)
    parser.add_argument("-C", "--compile", help="compilation script", type=str)
    parser.add_argument("-d", "--dir", help="directory to be mounted as /host", type=str)
    parser.add_argument("-i", "--image", help="DOCKER image")
    parser.add_argument("-k", "--kill", help="kill a job [--kill job_number]", type=str)
    parser.add_argument("-n", "--cores", help="number of cores for OAR [use 24 for a full node, 32 for the 'fat nodes']", type=str, default="1")
    parser.add_argument("-r", "--replicates", help="number of replicates", type=int, default=1)
    parser.add_argument("-S", "--script", help="script to compile and run", type=str)
    parser.add_argument("-s", "--submit", help="submit the job to OAR", action="store_true")
    parser.add_argument("-v", "--verbose", help="print more information", action="store_true")
    parser.add_argument("-w", "--walltime", help="walltime for the OAR job (warning the job will be killed after this time)", type=str, default="24:00")

    args = parser.parse_args()
    return args, parser



### main logic
args, parser = parse_args()

print("WARNING: comments are not allowd in scripts")

if args.kill:
    run("oardel -s SIGTERM " + args.kill, args.verbose)
    sys.exit(0)

if not args.image:
    print("ERROR: we need a docker image!")
    parser.print_help()
    sys.exit(1)

if not args.dir:
    print("ERROR: please specify a directory to be mounted in the image as /host!")
    parser.print_help()
    sys.exit(1)

if not args.cmd and not args.script and not args.compile:
    print("ERROR: we need a command or a script!")
    parser.print_help()
    sys.exit(1)

pwd = os.environ['HOME'] + '/tmp/'
if args.compile:
    s = make_docker_script(args, args.compile, pwd + "compile.sh", args.verbose)
    run("/bin/bash " + s, args.verbose)

if args.cmd:
    with open(pwd + "cmd.sh", 'w') as f:
        f.write(args.cmd + "\n")
    s = make_docker_script(args, pwd + "cmd.sh", pwd + "cmd.sh", args.verbose)
    run("/bin/bash " + s, args.verbose)

if args.script and not args.submit:
    print("script:", args.script)
    s = make_docker_script(args, args.script, pwd + "script.sh", args.verbose)
    run("/bin/bash " + s, args.verbose)

if args.script and args.submit:
    oarsub_args = "-l/nodes=1/core={},walltime={}".format(args.cores, args.walltime)
    s = make_docker_script(args, args.script, pwd + "script.sh", args.verbose)
    cmd = "oarsub " + oarsub_args + " \"/bin/bash " + s + "\""
    for i in range(0, args.replicates):
        run(cmd, args.verbose)


