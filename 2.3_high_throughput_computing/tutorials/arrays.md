# High-Throughput + Many-Task Computing

- [Batch job arrays](arrays.md)
- [Batch job dependencies](dependencies.md)
- [Batch job bundling](bundling.md)
- [Preemptible batch jobs](preemptible.md)

## Batch job arrays

Batch job arrays offer a mechanism for submitting and managing large
collections of similar jobs quickly and easily.

### Setting up an example problem: Estimating Pi

![Estimate the value of Pi via Monte Carlo](https://hpc.llnl.gov/sites/default/files/styles/no_sidebar_3_up/public/pi1.gif)

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

Next, navigate to the *scripts* directory and take a look at the `estimate-pi.sh` batch job script.

*Command*
```
cat estimate-pi.sh
```

*Output*
```
[mkandes@login02 ~]$ ls
data  projects  scratch  scripts  sdsc-summer-institute-2026  software
[mkandes@login02 ~]$ cd sdsc-summer-institute-2026/
[mkandes@login02 sdsc-summer-institute-2026]$ ls
0_Preparation                                 4.1_knowledge_management                     ccr_info.md
1.0_preparation_day_welcome_and_orientation   4.2_deep_learning_pt1                        HELPER_ONBOARDING.md
2.1_parallel_computing_concepts               4.3_deep_learning_pt2                        internship.md
2.2_running_batch_and_interactive_jobs        5.1_best_practices_for_scientific_computing  README.md
2.3_high_throughput_computing                 5.2_performance_tuning                       srun-compute.sh
2.4_code_migration_and_software_environments  5.3_gpu_computing_and_programming            srun-debug.sh
3.1_data_management                           6.1_python_for_HPC                           srun-gpu.sh
3.2_getting_help                              6.2_overview_of_sdsc_supercomputers          srun-shared.sh
3.3_parallel_computing_mpi_openmp             AGENDA.md
[mkandes@login02 sdsc-summer-institute-2026]$ cd 2.3_high_throughput_computing/
[mkandes@login02 2.3_high_throughput_computing]$ ls
code  README.md  scripts  tutorials
[mkandes@login02 2.3_high_throughput_computing]$ cd scripts/
[mkandes@login02 scripts]$ cat estimate-pi.sh 
#!/usr/bin/env bash

#SBATCH --job-name=estimate-pi
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%j.%N

module purge

time -p ../code/4pi/bash/pi.sh -b 8 -r 5 -s 10000
[mkandes@login02 scripts]$
```

Look at what variables the different command-line options are used to control in the problem. 

*Command*
```
head -n 15 ../code/4pi/bash/pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ head -n 15 ../code/4pi/bash/pi.sh
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
[mkandes@login02 scripts]$
```

Submit the batch job to the scheduler with the default settings. 

*Command*
```
sbatch estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh  estimate-pi.sh  pi-workflow.sh
[mkandes@login02 scripts]$ sbatch estimate-pi.sh 
Submitted batch job 52894884
[mkandes@login02 scripts]$
```

Monitor the job status in the queue.

*Command*
```
squeue --me
```

*Output*
```
[mkandes@login02 scripts]$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          52894884    shared estimate  mkandes  R       0:03      1 exp-1-08
[mkandes@login02 scripts]$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          52894884    shared estimate  mkandes  R       0:48      1 exp-1-08
[mkandes@login02 scripts]$
```

Check the standard output file for the results.

*Command*
```
cat estimate-pi.o*
```

*Output*
```
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh  estimate-pi.o52894884.exp-1-08  estimate-pi.sh  pi-workflow.sh
[mkandes@login02 scripts]$ cat estimate-pi.o* 
3.15040
real 58.03
user 34.14
sys 23.43
[mkandes@login02 scripts]$
```

### Creating your first job array

Modify the example batch job script to create your first array job (of 
10 array tasks).

*Command*
```
sed -i 's|#SBATCH --output=%x.o%j.%N|#SBATCH --output=%x.o%A.%a.%N|' estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ sed -i 's|#SBATCH --output=%x.o%j.%N|#SBATCH --output=%x.o%A.%a.%N|' estimate-pi.sh 
[mkandes@login02 scripts]$ cat estimate-pi.sh
#!/usr/bin/env bash

#SBATCH --job-name=estimate-pi
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%A.%a.%N

module purge

time -p ../code/4pi/bash/pi.sh -b 8 -r 5 -s 10000
[mkandes@login02 scripts]$
```

*Command*
```
sed -i '13i#SBATCH --array=0-9' estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ sed -i '13i#SBATCH --array=0-9' estimate-pi.sh
[mkandes@login02 scripts]$ cat estimate-pi.sh 
#!/usr/bin/env bash

#SBATCH --job-name=estimate-pi
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%A.%a.%N
#SBATCH --array=0-9

module purge

time -p ../code/4pi/bash/pi.sh -b 8 -r 5 -s 10000
[mkandes@login02 scripts]$
```

Submit the modified batch job script to the scheduler.

*Command*
```
sbatch estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh  estimate-pi.o52894884.exp-1-08  estimate-pi.sh  pi-workflow.sh
[mkandes@login02 scripts]$ sbatch estimate-pi.sh 
Submitted batch job 52895363
[mkandes@login02 scripts]$
```

Check the status of the job array in the queue.

*Command*
```
squeue --me
```

*Output*
```
[mkandes@login02 scripts]$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        52895363_0    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_1    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_2    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_3    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_4    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_5    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_6    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_7    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_8    shared estimate  mkandes  R       0:41      1 exp-1-08
        52895363_9    shared estimate  mkandes  R       0:41      1 exp-1-08
[mkandes@login02 scripts]$
```

Once the job array and all of its tasks complete, check the results.

*Command*
```
head -n 1 estimate-pi.o* -q
```

```
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh               estimate-pi.o52895363.2.exp-1-08  estimate-pi.o52895363.6.exp-1-08  estimate-pi.sh
estimate-pi.o52894884.exp-1-08    estimate-pi.o52895363.3.exp-1-08  estimate-pi.o52895363.7.exp-1-08  pi-workflow.sh
estimate-pi.o52895363.0.exp-1-08  estimate-pi.o52895363.4.exp-1-08  estimate-pi.o52895363.8.exp-1-08
estimate-pi.o52895363.1.exp-1-08  estimate-pi.o52895363.5.exp-1-08  estimate-pi.o52895363.9.exp-1-08
[mkandes@login02 scripts]$ head -n 1 estimate-pi.o* -q
3.15040
3.12680
3.14960
3.14400
3.13800
3.15120
3.14440
3.11200
3.14160
3.14920
3.15880
[mkandes@login02 scripts]$
```

Next check the runtime of each array task.

*Command*
```
grep 'real' estimate-pi.o*
```

*Output*
```
[mkandes@login02 scripts]$ grep 'real' estimate-pi.o*
estimate-pi.o52894884.exp-1-08:real 58.03
estimate-pi.o52895363.0.exp-1-08:real 90.59
estimate-pi.o52895363.1.exp-1-08:real 90.32
estimate-pi.o52895363.2.exp-1-08:real 89.83
estimate-pi.o52895363.3.exp-1-08:real 90.28
estimate-pi.o52895363.4.exp-1-08:real 91.79
estimate-pi.o52895363.5.exp-1-08:real 91.54
estimate-pi.o52895363.6.exp-1-08:real 91.72
estimate-pi.o52895363.7.exp-1-08:real 91.50
estimate-pi.o52895363.8.exp-1-08:real 93.02
estimate-pi.o52895363.9.exp-1-08:real 92.92
[mkandes@login02 scripts]$
```

### Using a job array to create a parameter sweep

Modify the array job script to create a parameter sweep over the `-b | --bytes` size variable using non-consecutive array index values and the `SLURM_ARRAY_TASK_ID` environment variable.

*Command*
```
sed -i 's|#SBATCH --array=0-9|#SBATCH --array=1,2,4,8|' estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ sed -i 's|#SBATCH --array=0-9|#SBATCH --array=1,2,4,8|' estimate-pi.sh 
[mkandes@login02 scripts]$ cat estimate-pi.sh 
#!/usr/bin/env bash

#SBATCH --job-name=estimate-pi
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%A.%a.%N
#SBATCH --array=1,2,4,8

module purge

time -p ../code/4pi/bash/pi.sh -b 8 -r 5 -s 10000
[mkandes@login02 scripts]$
```

*Command*
```
sed -i 's|-b 8|-b "${SLURM_ARRAY_TASK_ID}"|' estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ sed -i 's|-b 8|-b "${SLURM_ARRAY_TASK_ID}"|' estimate-pi.sh 
[mkandes@login02 scripts]$ cat estimate-pi.sh 
#!/usr/bin/env bash

#SBATCH --job-name=estimate-pi
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%A.%a.%N
#SBATCH --array=1,2,4,8

module purge

time -p ../code/4pi/bash/pi.sh -b "${SLURM_ARRAY_TASK_ID}" -r 5 -s 10000
[mkandes@login02 scripts]$
```

Submit the modified array job script to the scheduler.

*Command*
```
sbatch estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh               estimate-pi.o52895363.2.exp-1-08  estimate-pi.o52895363.6.exp-1-08  estimate-pi.sh
estimate-pi.o52894884.exp-1-08    estimate-pi.o52895363.3.exp-1-08  estimate-pi.o52895363.7.exp-1-08  pi-workflow.sh
estimate-pi.o52895363.0.exp-1-08  estimate-pi.o52895363.4.exp-1-08  estimate-pi.o52895363.8.exp-1-08
estimate-pi.o52895363.1.exp-1-08  estimate-pi.o52895363.5.exp-1-08  estimate-pi.o52895363.9.exp-1-08
[mkandes@login02 scripts]$ sbatch estimate-pi.sh 
Submitted batch job 52895472
[mkandes@login02 scripts]$
```

And then monitor the status of the job in queue.

*Command*
```
squeue --me
```

*Ouput*
```
[mkandes@login02 scripts]$ sbatch estimate-pi.sh 
Submitted batch job 52895472
[mkandes@login02 scripts]$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        52895472_1    shared estimate  mkandes  R       0:18      1 exp-1-08
        52895472_2    shared estimate  mkandes  R       0:18      1 exp-1-08
        52895472_4    shared estimate  mkandes  R       0:18      1 exp-1-08
        52895472_8    shared estimate  mkandes  R       0:18      1 exp-1-08
[mkandes@login02 scripts]$
```

Check the results.

*Command*
```
head -n 2 estimate-pi.o52895472.*
```

*Output*
```
[mkandes@login02 scripts]$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh               estimate-pi.o52895363.3.exp-1-08  estimate-pi.o52895363.8.exp-1-08  estimate-pi.o52895472.8.exp-1-08
estimate-pi.o52894884.exp-1-08    estimate-pi.o52895363.4.exp-1-08  estimate-pi.o52895363.9.exp-1-08  estimate-pi.sh
estimate-pi.o52895363.0.exp-1-08  estimate-pi.o52895363.5.exp-1-08  estimate-pi.o52895472.1.exp-1-08  pi-workflow.sh
estimate-pi.o52895363.1.exp-1-08  estimate-pi.o52895363.6.exp-1-08  estimate-pi.o52895472.2.exp-1-08
estimate-pi.o52895363.2.exp-1-08  estimate-pi.o52895363.7.exp-1-08  estimate-pi.o52895472.4.exp-1-08
[mkandes@login02 scripts]$ head -n 2 estimate-pi.o52895472.*
==> estimate-pi.o52895472.1.exp-1-08 <==
3.12880
real 58.79

==> estimate-pi.o52895472.2.exp-1-08 <==
3.12880
real 58.91

==> estimate-pi.o52895472.4.exp-1-08 <==
3.12720
real 58.99

==> estimate-pi.o52895472.8.exp-1-08 <==
3.14880
real 59.21
[mkandes@login02 scripts]$
```

Next, reset the `-b | --bytes` parameter to `8` and then rewrite the batch job script 
to create a parameter sweep over `-s | --samples` variable. However, in this case, 
use the `SLURM_ARRAY_TASK_ID` to logarithmically scale the number of samples.

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
