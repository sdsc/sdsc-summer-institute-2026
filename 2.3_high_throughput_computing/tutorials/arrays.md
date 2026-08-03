# High-Throughput + Many-Task Computing

- [Batch job arrays](arrays.md)
- [Batch job dependencies](dependencies.md)
- [Batch job bundling](bundling.md)
- [Preemptible batch jobs](preemptible.md)

## Batch job arrays

Batch job arrays offer a mechanism for submitting and managing large
collections of similar jobs quickly and easily.

### Setting up an example problem: Estimating Pi

Login to Expanse via SSH or the [Expanse User Portal](https://portal.expanse.sdsc.edu).

*Command*
```
ssh mkandes@login.expanse.sdsc.edu
```

*Output*
```
mkandes@hardtack:~$ ssh mkandes@login.expanse.sdsc.edu
(mkandes@login.expanse.sdsc.edu) TOTP code for mkandes: 267577
Welcome to Bright release         9.0

                                                         Based on Rocky Linux 8
                                                                    ID: #000002

--------------------------------------------------------------------------------

                                 WELCOME TO
                  _______  __ ____  ___    _   _______ ______
                 / ____/ |/ // __ \/   |  / | / / ___// ____/
                / __/  |   // /_/ / /| | /  |/ /\__ \/ __/
               / /___ /   |/ ____/ ___ |/ /|  /___/ / /___
              /_____//_/|_/_/   /_/  |_/_/ |_//____/_____/

--------------------------------------------------------------------------------

Use the following commands to adjust your environment:

'module avail'            - show available modules
'module add <module>'     - adds a module to your environment for this session
'module initadd <module>' - configure module to be loaded at every login

-------------------------------------------------------------------------------
Last login: Sun Aug  2 20:15:11 2026 from 136.26.86.246
[mkandes@login01 ~]$
```

If you are using the Expanse User Portal, open the *Expanse Shell Access*
app once you are logged in.

[4pi](https://github.com/mkandes/4pi) is a collection of simple computer
programs that estimate the value of Pi. Each program in the collection
differs only in the programming language it was written in, the set of
features of the language it utilized, and/or the fundamental underlying
mathematical algorithm it implemented to approximate the value of Pi. We
will estiamte the value of Pi via a Monte Carlo method.

![Estimate the value of Pi via Monte Carlo](https://hpc.llnl.gov/sites/default/files/styles/no_sidebar_3_up/public/pi1.gif)

Inspect the job script.

```
[xdtr108@login01 ~]$ cat estimate-pi.sh 
#!/usr/bin/env bash

#SBATCH --job-name=estimate-pi
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:30:00
#SBATCH --output=%x.o%j.%N

module purge

time -p "${HOME}/4pi/bash/pi.sh" -b 8 -r 5 -s 10000
```

Investigate what variables the different command-line options are used to control in the problem. 

```
head -n 15 "${HOME}/4pi/bash/pi.sh"
```

```
[xdtr108@login01 ~]$ head -n 15 "${HOME}/4pi/bash/pi.sh"
#!/usr/bin/env bash
#
# Estimate the value of Pi via Monte Carlo

# Read in and parse input variables from command-line arguments
if (( "${#}" > 0 )); then
  while (( "${#}" > 0 )); do
    case "${1}" in
      -b | --bytes ) bytes="${2}" ;;
      -r | --round ) round="${2}" ;;
      -s | --samples ) samples="${2}" ;;
    esac
    shift 2
  done
fi
```

Submit the batch job to the scheduler with the default settings. 

```
[xdtr108@login01 ~]$ sbatch estimate-pi.sh 
Submitted batch job 14791638
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          14791638     debug estimate  xdtr108  R       0:05      1 exp-9-55
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          14791638     debug estimate  xdtr108 CG       0:51      1 exp-9-55
[xdtr108@login01 ~]$ ls
4pi  estimate-pi.o14791638.exp-9-55  estimate-pi.sh
```

Check the standard output file for the results.

```
[xdtr108@login01 ~]$ cat estimate-pi.o14791638.exp-9-55 
3.12160
real 50.12
user 32.41
sys 17.21
```

### Creating your first job array

Modify the example batch job script to create your first array job (of 
10 array tasks). 

```
#SBATCH --output=%x.o%A.%a.%N
#SBATCH --array=0-9
```

Submit the modified batch job script to the scheduler.

```
[xdtr108@login01 ~]$ cat estimate-pi.sh 
#!/usr/bin/env bash

#SBATCH --job-name=estimate-pi
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:30:00
#SBATCH --output=%x.o%A.%a.%N
#SBATCH --array=0-9

module purge

time -p "${HOME}/4pi/bash/pi.sh" -b 8 -r 5 -s 10000
[xdtr108@login01 ~]$ sbatch estimate-pi.sh 
Submitted batch job 14791898
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14791898_8    shared estimate  xdtr108  R       0:00      1 exp-1-06
        14791898_9    shared estimate  xdtr108  R       0:00      1 exp-1-06
        14791898_0    shared estimate  xdtr108  R       0:01      1 exp-1-06
        14791898_1    shared estimate  xdtr108  R       0:01      1 exp-1-06
        14791898_2    shared estimate  xdtr108  R       0:01      1 exp-1-06
        14791898_3    shared estimate  xdtr108  R       0:01      1 exp-1-06
        14791898_4    shared estimate  xdtr108  R       0:01      1 exp-1-06
        14791898_5    shared estimate  xdtr108  R       0:01      1 exp-1-06
        14791898_6    shared estimate  xdtr108  R       0:01      1 exp-1-06
        14791898_7    shared estimate  xdtr108  R       0:01      1 exp-1-06
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14791898_7    shared estimate  xdtr108 CG       1:27      1 exp-1-06
        14791898_8    shared estimate  xdtr108  R       1:26      1 exp-1-06
        14791898_9    shared estimate  xdtr108  R       1:26      1 exp-1-06
        14791898_0    shared estimate  xdtr108  R       1:27      1 exp-1-06
        14791898_1    shared estimate  xdtr108  R       1:27      1 exp-1-06
        14791898_2    shared estimate  xdtr108  R       1:27      1 exp-1-06
        14791898_3    shared estimate  xdtr108  R       1:27      1 exp-1-06
        14791898_4    shared estimate  xdtr108  R       1:27      1 exp-1-06
        14791898_5    shared estimate  xdtr108  R       1:27      1 exp-1-06
        14791898_6    shared estimate  xdtr108  R       1:27      1 exp-1-06
[xdtr108@login01 ~]$ ls
4pi                               estimate-pi.o14791898.5.exp-1-06
estimate-pi.o14791638.exp-9-55    estimate-pi.o14791898.6.exp-1-06
estimate-pi.o14791898.0.exp-1-06  estimate-pi.o14791898.7.exp-1-06
estimate-pi.o14791898.1.exp-1-06  estimate-pi.o14791898.8.exp-1-06
estimate-pi.o14791898.2.exp-1-06  estimate-pi.o14791898.9.exp-1-06
estimate-pi.o14791898.3.exp-1-06  estimate-pi.sh
estimate-pi.o14791898.4.exp-1-06
```

Check the results from the job array ... 

```
[xdtr108@login01 ~]$ head -n 1 estimate-pi.o14791898.* -q
3.14480
3.16840
3.15480
3.17200
3.13480
3.15480
3.17840
3.12800
3.14080
3.16000
```

... and the runtimes of each array task.

```
[xdtr108@login01 ~]$ grep 'real' estimate-pi.o14791898.*
estimate-pi.o14791898.0.exp-1-06:real 85.82
estimate-pi.o14791898.1.exp-1-06:real 86.05
estimate-pi.o14791898.2.exp-1-06:real 85.94
estimate-pi.o14791898.3.exp-1-06:real 86.17
estimate-pi.o14791898.4.exp-1-06:real 85.80
estimate-pi.o14791898.5.exp-1-06:real 85.80
estimate-pi.o14791898.6.exp-1-06:real 85.82
estimate-pi.o14791898.7.exp-1-06:real 85.79
estimate-pi.o14791898.8.exp-1-06:real 86.55
estimate-pi.o14791898.9.exp-1-06:real 86.43
```

### Using a job array to create a parameter sweep

Modify the array job script to create a parameter sweep over the `-b | --bytes` size variable using non-consecutive array index values and the `SLURM_ARRAY_TASK_ID` environment variable.

```
#SBATCH --array=1,2,4,8

module purge

time -p "${HOME}/4pi/bash/pi.sh" -b "${SLURM_ARRAY_TASK_ID}" -r 5 -s 10000
```

Submit the modified array job script to the scheduler.

```
[xdtr108@login01 ~]$ sbatch estimate-pi.sh 
Submitted batch job 14792416
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14792416_8    shared estimate  xdtr108 PD       0:00      1 (None)
        14792416_4    shared estimate  xdtr108 PD       0:00      1 (None)
        14792416_2    shared estimate  xdtr108 PD       0:00      1 (None)
        14792416_1    shared estimate  xdtr108 PD       0:00      1 (None)
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14792416_1    shared estimate  xdtr108  R       0:08      1 exp-1-06
        14792416_2    shared estimate  xdtr108  R       0:08      1 exp-1-06
        14792416_4    shared estimate  xdtr108  R       0:08      1 exp-1-06
        14792416_8    shared estimate  xdtr108  R       0:08      1 exp-1-06
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14792416_1    shared estimate  xdtr108  R       1:22      1 exp-1-06
[xdtr108@login01 ~]$ ls
4pi                               estimate-pi.o14791898.7.exp-1-06
estimate-pi.o14791638.exp-9-55    estimate-pi.o14791898.8.exp-1-06
estimate-pi.o14791898.0.exp-1-06  estimate-pi.o14791898.9.exp-1-06
estimate-pi.o14791898.1.exp-1-06  estimate-pi.o14792416.1.exp-1-06
estimate-pi.o14791898.2.exp-1-06  estimate-pi.o14792416.2.exp-1-06
estimate-pi.o14791898.3.exp-1-06  estimate-pi.o14792416.4.exp-1-06
estimate-pi.o14791898.4.exp-1-06  estimate-pi.o14792416.8.exp-1-06
estimate-pi.o14791898.5.exp-1-06  estimate-pi.sh
estimate-pi.o14791898.6.exp-1-06
```

Check the results. 

```
[xdtr108@login01 ~]$ head -n 2 estimate-pi.o14792416.*
==> estimate-pi.o14792416.1.exp-1-06 <==
3.13840
real 88.80

==> estimate-pi.o14792416.2.exp-1-06 <==
3.12880
real 70.73

==> estimate-pi.o14792416.4.exp-1-06 <==
3.16040
real 70.61

==> estimate-pi.o14792416.8.exp-1-06 <==
3.15280
real 70.82
```

Next, reset the `-b | --bytes` parameter to `8` and then rewrite the batch job script to create a parameter sweep over `-s | --samples` variable. However, in this case, use the `SLURM_ARRAY_TASK_ID` to logarithmically scale the number of samples.

```
#SBATCH --array=1,10,100,1000,10000

module purge

time -p "${HOME}/4pi/bash/pi.sh" -b 8 -r 5 -s "${SLURM_ARRAY_TASK_ID}"
```

```
[xdtr108@login01 ~]$ sbatch estimate-pi.sh 
sbatch: error: Batch job submission failed: Invalid job array specification
[xdtr108@login01 ~]$
```

What went wrong?

```
[xdtr108@login01 ~]$ ls -l /etc/slurm/
total 0
[xdtr108@login01 ~]$ echo $SLURM_CONF
/cm/shared/apps/slurm/var/etc/expanse/slurm.conf
[xdtr108@login01 ~]$ cat $SLURM_CONF | grep MaxArraySize
MaxArraySize=1000
```

```
[xdtr108@login01 ~]$ cat $SLURM_CONF | grep MaxJobCount
MaxJobCount=40000
```

What is the solution? Reindex using another environment variable based on your `SLURM_ARRAY_TASK_ID`.

```
#SBATCH --array=1-5

declare -xir NUMBER_OF_SAMPLES="10**${SLURM_ARRAY_TASK_ID}"

module purge

time -p "${HOME}/4pi/bash/pi.sh" -b 8 -r 5 -s "${NUMBER_OF_SAMPLES}"
```

- https://google.github.io/styleguide/shellguide.html

```
[xdtr108@login01 ~]$ sbatch estimate-pi.sh 
Submitted batch job 14792680
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14792680_5    shared estimate  xdtr108 PD       0:00      1 (None)
        14792680_4    shared estimate  xdtr108 PD       0:00      1 (None)
        14792680_3    shared estimate  xdtr108 PD       0:00      1 (None)
        14792680_2    shared estimate  xdtr108 PD       0:00      1 (None)
        14792680_1    shared estimate  xdtr108 PD       0:00      1 (None)
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14792680_5    shared estimate  xdtr108 PD       0:00      1 (Priority)
        14792680_4    shared estimate  xdtr108 PD       0:00      1 (Priority)
        14792680_3    shared estimate  xdtr108 PD       0:00      1 (Priority)
        14792680_2    shared estimate  xdtr108 PD       0:00      1 (Priority)
        14792680_1    shared estimate  xdtr108 PD       0:00      1 (Priority)
[xdtr108@login01 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        14792680_5    shared estimate  xdtr108  R       3:03      1 exp-1-06
[xdtr108@login02 ~]$ ls
4pi                               estimate-pi.o14791898.9.exp-1-06
estimate-pi.o14791638.exp-9-55    estimate-pi.o14792416.1.exp-1-06
estimate-pi.o14791898.0.exp-1-06  estimate-pi.o14792416.2.exp-1-06
estimate-pi.o14791898.1.exp-1-06  estimate-pi.o14792416.4.exp-1-06
estimate-pi.o14791898.2.exp-1-06  estimate-pi.o14792416.8.exp-1-06
estimate-pi.o14791898.3.exp-1-06  estimate-pi.o14792680.1.exp-1-06
estimate-pi.o14791898.4.exp-1-06  estimate-pi.o14792680.2.exp-1-06
estimate-pi.o14791898.5.exp-1-06  estimate-pi.o14792680.3.exp-1-06
estimate-pi.o14791898.6.exp-1-06  estimate-pi.o14792680.4.exp-1-06
estimate-pi.o14791898.7.exp-1-06  estimate-pi.o14792680.5.exp-1-06
estimate-pi.o14791898.8.exp-1-06  estimate-pi.sh
[xdtr108@login02 ~]$
```

```
[xdtr108@login02 ~]$ head -n 2 estimate-pi.o14792680.*
==> estimate-pi.o14792680.1.exp-1-06 <==
2.80000
real 0.08

==> estimate-pi.o14792680.2.exp-1-06 <==
3.08000
real 0.54

==> estimate-pi.o14792680.3.exp-1-06 <==
3.20400
real 5.57

==> estimate-pi.o14792680.4.exp-1-06 <==
3.11880
real 50.96

==> estimate-pi.o14792680.5.exp-1-06 <==
3.14632
real 535.73
[xdtr108@login02 ~]$
```

### Throttling a large array job

Let's migrate from the (slow) bash-based Pi program to the (faster)
python one for a better estimate. We'll then create a large array job,
but throttle the number of jobs that can run simultaneosuly. 

```
#SBATCH --array=1-512%32

module purge

time -p python3 "${HOME}/4pi/python/pi.py" 100000000
```

```
[xdtr108@login02 ~]$ sbatch estimate-pi.sh 
Submitted batch job 14799628
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
  14799628_[1-512]    shared estimate  xdtr108 PD       0:00      1 (None)
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
 14799628_[30-512]    shared estimate  xdtr108 PD       0:00      1 (Priority)
        14799628_1    shared estimate  xdtr108  R       0:09      1 exp-1-06
        14799628_2    shared estimate  xdtr108  R       0:09      1 exp-1-06
        14799628_3    shared estimate  xdtr108  R       0:09      1 exp-1-06
        14799628_4    shared estimate  xdtr108  R       0:09      1 exp-1-12
        14799628_5    shared estimate  xdtr108  R       0:09      1 exp-1-12
        14799628_6    shared estimate  xdtr108  R       0:09      1 exp-1-12
        ...
       14799628_27    shared estimate  xdtr108  R       0:09      1 exp-1-34
       14799628_28    shared estimate  xdtr108  R       0:09      1 exp-1-34
       14799628_29    shared estimate  xdtr108  R       0:09      1 exp-1-34
 [xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
 14799628_[62-512]    shared estimate  xdtr108 PD       0:00      1 (JobArrayTaskLimit)
       14799628_37    shared estimate  xdtr108  R       0:23      1 exp-1-34
       14799628_38    shared estimate  xdtr108  R       0:23      1 exp-1-34
       14799628_39    shared estimate  xdtr108  R       0:23      1 exp-1-34
       14799628_40    shared estimate  xdtr108  R       0:23      1 exp-1-34
       ...
       14799628_35    shared estimate  xdtr108  R       0:24      1 exp-1-27
       14799628_36    shared estimate  xdtr108  R       0:24      1 exp-1-34
[xdtr108@login02 ~]$ scancel 14799628_[256-512]
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
      14799628_255    shared estimate  xdtr108 PD       0:00      1 (JobArrayTaskLimit)
      14799628_254    shared estimate  xdtr108 PD       0:00      1 (JobArrayTaskLimit)
      14799628_253    shared estimate  xdtr108 PD       0:00      1 (JobArrayTaskLimit)
      ...
       14799628_84    shared estimate  xdtr108  R       0:02      1 exp-1-27
       14799628_85    shared estimate  xdtr108  R       0:02      1 exp-1-27
       14799628_86    shared estimate  xdtr108  R       0:02      1 exp-1-34
[xdtr108@login02 ~]$ scancel 14799628
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
       14799628_87    shared estimate  xdtr108 CG       0:29      1 exp-1-34
       14799628_88    shared estimate  xdtr108 CG       0:29      1 exp-1-34
       14799628_89    shared estimate  xdtr108 CG       0:29      1 exp-1-34
       ...
       14799628_85    shared estimate  xdtr108 CG       0:30      1 exp-1-27
       14799628_86    shared estimate  xdtr108 CG       0:30      1 exp-1-34
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
[xdtr108@login02 ~]$ ls
4pi                                estimate-pi.o14799628.44.exp-1-34
estimate-pi.o14791638.exp-9-55     estimate-pi.o14799628.45.exp-1-34
estimate-pi.o14791898.0.exp-1-06   estimate-pi.o14799628.46.exp-1-34
estimate-pi.o14791898.1.exp-1-06   estimate-pi.o14799628.47.exp-1-34
estimate-pi.o14791898.2.exp-1-06   estimate-pi.o14799628.48.exp-1-34
estimate-pi.o14791898.3.exp-1-06   estimate-pi.o14799628.49.exp-1-34
estimate-pi.o14791898.4.exp-1-06   estimate-pi.o14799628.4.exp-1-12
estimate-pi.o14791898.5.exp-1-06   estimate-pi.o14799628.50.exp-1-34
estimate-pi.o14791898.6.exp-1-06   estimate-pi.o14799628.51.exp-1-34
...
estimate-pi.o14799628.40.exp-1-34  estimate-pi.o14799628.93.exp-1-34
estimate-pi.o14799628.41.exp-1-34  estimate-pi.o14799628.9.exp-1-15
estimate-pi.o14799628.42.exp-1-34  estimate-pi.sh
estimate-pi.o14799628.43.exp-1-34
```

```
[xdtr108@login02 ~]$ head -n 2 estimate-pi.o14799628.*
==> estimate-pi.o14799628.10.exp-1-27 <==
3.141280711412807
real 52.23

==> estimate-pi.o14799628.11.exp-1-27 <==
3.14126499141265
real 51.66

==> estimate-pi.o14799628.12.exp-1-27 <==
3.1412676714126766
real 54.90
...
```


#

Next - [Batch job dependencies](dependencies.md)
