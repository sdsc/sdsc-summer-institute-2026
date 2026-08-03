# High-Throughput + Many-Task Computing

- [Batch job arrays](arrays.md)
- [Batch job dependencies](dependencies.md)
- [Batch job bundling](bundling.md)
- [Preemptible batch jobs](preemptible.md)

## Batch job dependencies

Batch job dependencies are useful when you need to run multiple jobs in
a particular order. A standard example of this is a workflow or pipeline
in which the output from one or more jobs is used as the input to the next. 
Rather than manually checking the job queue yourself from time to time to
see if one job has ended and then manually submit the next, all the jobs 
in the workflow can be submitted at once. The scheduler will then manage
the jobs for you and run them in the proper order based on the conditions
you have applied to the jobs.  

SLURM's built-in job dependencies are used to defer the start of a job 
until the specified dependencies have been satisfied. They are specified
with the `-d | --dependency` option to the `sbatch` command.

```
sbatch --dependency=<dependency_list> dependent-job.sh
```

The format of the `<dependency_list>` is of the form  
`<type:job_id[:job_id][,type:job_id[:job_id]]>` or 
`<type:job_id[:job_id][?type:job_id[:job_id]]>`. Note that all 
dependencies must be satisfied if the `,` separator is used. In contrast,
any dependency may be satisfied if the `?` separator is used. Only one
separator may be used. Many jobs can share the same dependency and these
jobs may even belong to different users. Once a job dependency fails due
to the termination state of a preceding job, *the dependent job will never run.*

The job dependency types supported by SLURM are:

- **after** - This job can begin execution after the specified job(s)
  have begun execution. 
- **afterany** - This job can begin execution after the specified job(s)
  have terminated.
- **aftercorr** - A task of this job array can begin execution after the
  corresponding task ID in the specified job has completed successfully
  (ran to completion with an exit code of zero).
- **afternotok** - This job can begin execution after the specified job(s)
  have terminated in some failed state (non-zero exit code, node failure, 
  timed out, etc). 
- **afterok** - This job can begin execution after the specified jobs have
  successfully executed (ran to completion with an exit code of zero).
- **singleton** - This job can begin execution after any previously launched
  jobs sharing the same job name and user have terminated.  In other words,
  only one job by that name and owned by that user can be running or
  suspended at any point in time.

### Create your first job dependency

Before we begin, let's first clean up your working direcotry by deleting all
of the standard output files from the array job exercies we completed in
the previous section. 

*Command*
```
rm *.exp-*
```

*Output*
```
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh                estimate-pi.o52895833.19.exp-1-29  estimate-pi.o52895833.46.exp-1-38  estimate-pi.o52895833.73.exp-1-42
estimate-pi.o52894884.exp-1-08     estimate-pi.o52895833.1.exp-1-29   estimate-pi.o52895833.47.exp-1-38  estimate-pi.o52895833.74.exp-1-42
estimate-pi.o52895363.0.exp-1-08   estimate-pi.o52895833.20.exp-1-29  estimate-pi.o52895833.48.exp-1-38  estimate-pi.o52895833.75.exp-1-42
estimate-pi.o52895363.1.exp-1-08   estimate-pi.o52895833.21.exp-1-29  estimate-pi.o52895833.49.exp-1-38  estimate-pi.o52895833.76.exp-1-42
estimate-pi.o52895363.2.exp-1-08   estimate-pi.o52895833.22.exp-1-29  estimate-pi.o52895833.4.exp-1-29   estimate-pi.o52895833.77.exp-1-42
estimate-pi.o52895363.3.exp-1-08   estimate-pi.o52895833.23.exp-1-29  estimate-pi.o52895833.50.exp-1-38  estimate-pi.o52895833.78.exp-1-29
estimate-pi.o52895363.4.exp-1-08   estimate-pi.o52895833.24.exp-1-29  estimate-pi.o52895833.51.exp-1-38  estimate-pi.o52895833.79.exp-1-29
estimate-pi.o52895363.5.exp-1-08   estimate-pi.o52895833.25.exp-1-29  estimate-pi.o52895833.52.exp-1-38  estimate-pi.o52895833.7.exp-1-29
estimate-pi.o52895363.6.exp-1-08   estimate-pi.o52895833.26.exp-1-29  estimate-pi.o52895833.53.exp-1-38  estimate-pi.o52895833.80.exp-1-29
estimate-pi.o52895363.7.exp-1-08   estimate-pi.o52895833.27.exp-1-29  estimate-pi.o52895833.54.exp-1-38  estimate-pi.o52895833.81.exp-1-29
estimate-pi.o52895363.8.exp-1-08   estimate-pi.o52895833.28.exp-1-29  estimate-pi.o52895833.55.exp-1-38  estimate-pi.o52895833.82.exp-1-29
estimate-pi.o52895363.9.exp-1-08   estimate-pi.o52895833.29.exp-1-29  estimate-pi.o52895833.56.exp-1-38  estimate-pi.o52895833.83.exp-1-29
estimate-pi.o52895472.1.exp-1-08   estimate-pi.o52895833.2.exp-1-29   estimate-pi.o52895833.57.exp-1-29  estimate-pi.o52895833.84.exp-1-42
estimate-pi.o52895472.2.exp-1-08   estimate-pi.o52895833.30.exp-1-29  estimate-pi.o52895833.58.exp-1-29  estimate-pi.o52895833.85.exp-1-42
estimate-pi.o52895472.4.exp-1-08   estimate-pi.o52895833.31.exp-1-29  estimate-pi.o52895833.59.exp-1-38  estimate-pi.o52895833.86.exp-1-42
estimate-pi.o52895472.8.exp-1-08   estimate-pi.o52895833.32.exp-1-29  estimate-pi.o52895833.5.exp-1-29   estimate-pi.o52895833.87.exp-1-29
estimate-pi.o52895589.1.exp-1-38   estimate-pi.o52895833.33.exp-1-29  estimate-pi.o52895833.60.exp-1-38  estimate-pi.o52895833.88.exp-1-29
estimate-pi.o52895589.2.exp-1-38   estimate-pi.o52895833.34.exp-1-38  estimate-pi.o52895833.61.exp-1-38  estimate-pi.o52895833.89.exp-1-29
estimate-pi.o52895589.3.exp-1-38   estimate-pi.o52895833.35.exp-1-38  estimate-pi.o52895833.62.exp-1-38  estimate-pi.o52895833.8.exp-1-29
estimate-pi.o52895589.4.exp-1-38   estimate-pi.o52895833.36.exp-1-38  estimate-pi.o52895833.63.exp-1-38  estimate-pi.o52895833.90.exp-1-29
estimate-pi.o52895589.5.exp-1-38   estimate-pi.o52895833.37.exp-1-38  estimate-pi.o52895833.64.exp-1-38  estimate-pi.o52895833.91.exp-1-29
estimate-pi.o52895833.10.exp-1-29  estimate-pi.o52895833.38.exp-1-38  estimate-pi.o52895833.65.exp-1-29  estimate-pi.o52895833.92.exp-1-29
estimate-pi.o52895833.11.exp-1-29  estimate-pi.o52895833.39.exp-1-38  estimate-pi.o52895833.66.exp-1-29  estimate-pi.o52895833.93.exp-1-29
estimate-pi.o52895833.12.exp-1-29  estimate-pi.o52895833.3.exp-1-29   estimate-pi.o52895833.67.exp-1-29  estimate-pi.o52895833.94.exp-1-29
estimate-pi.o52895833.13.exp-1-29  estimate-pi.o52895833.40.exp-1-38  estimate-pi.o52895833.68.exp-1-29  estimate-pi.o52895833.95.exp-1-29
estimate-pi.o52895833.14.exp-1-29  estimate-pi.o52895833.41.exp-1-38  estimate-pi.o52895833.69.exp-1-29  estimate-pi.o52895833.96.exp-1-29
estimate-pi.o52895833.15.exp-1-29  estimate-pi.o52895833.42.exp-1-38  estimate-pi.o52895833.6.exp-1-29   estimate-pi.o52895833.9.exp-1-29
estimate-pi.o52895833.16.exp-1-29  estimate-pi.o52895833.43.exp-1-38  estimate-pi.o52895833.70.exp-1-29  estimate-pi.sh
estimate-pi.o52895833.17.exp-1-29  estimate-pi.o52895833.44.exp-1-38  estimate-pi.o52895833.71.exp-1-29  pi-workflow.sh
estimate-pi.o52895833.18.exp-1-29  estimate-pi.o52895833.45.exp-1-38  estimate-pi.o52895833.72.exp-1-29
[mkandes@login02 scripts]$ rm *.exp-*
[mkandes@login02 scripts]$ ls
compute-pi-stats.sh  estimate-pi.sh  pi-workflow.sh
[mkandes@login02 scripts]$
```

Next, shrink the large array job down quite a bit.

*Command*
```
sed -i 's|#SBATCH --array=1-512%32|#SBATCH --array=1-20%10|' estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ sed -i 's|#SBATCH --array=1-512%32|#SBATCH --array=1-20%10|' estimate-pi.sh 
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
#SBATCH --array=1-20%10

module purge

time -p ../code/4pi/python/pi.py 100000000
[mkandes@login02 scripts]$
```

Next, inspect the `compute-pi-stats.sh` job script.

*Command*
```
cat compute-pi-stats.sh
```

*Output*
```
[mkandes@login02 scripts]$ cat compute-pi-stats.sh
#!/usr/bin/env bash

#SBATCH --job-name=compute-pi-stats
#SBATCH --account=sdp173
#SBATCH --reservation=si26cpu
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%j.%N

declare -xir DEPENDENT_SLURM_ARRAY_JOB_ID="${1}"

module reset
module load gcc/10.2.0
module load gnuplot/5.4.2

echo "$(cat estimate-pi.o${DEPENDENT_SLURM_ARRAY_JOB_ID}.*)" | \
  gnuplot -e 'stats "-"; print STATS_mean, STATS_stddev'
[mkandes@login02 scripts]$
```

With both batch job scripts in place, launch the array job. 

*Command*
```
sbatch estimate-pi.sh
```

*Output*
```
[mkandes@login02 scripts]$ sbatch estimate-pi.sh 
Submitted batch job 52896226
[mkandes@login02 scripts]$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
       52896226_20    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_19    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_18    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_17    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_16    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_15    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_14    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_13    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_12    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
       52896226_11    shared estimate  mkandes PD       0:00      1 (JobArrayTaskLimit)
        52896226_1    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_2    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_3    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_4    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_5    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_6    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_7    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_8    shared estimate  mkandes  R       0:30      1 exp-1-29
        52896226_9    shared estimate  mkandes  R       0:30      1 exp-1-29
       52896226_10    shared estimate  mkandes  R       0:30      1 exp-1-29
[mkandes@login02 scripts]$
```



Then submit the stats job to run after all of the array tasks complete successfully. 

*Command*
```
sbatch --dependency=afterok:52896226 compute-pi-stats.sh 52896226
```

*Output*
```
[mkandes@login02 scripts]$ sbatch --dependency=afterok:52896226 compute-pi-stats.sh 52896226
Submitted batch job 52896252
[mkandes@login02 scripts]$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          52896252    shared compute-  mkandes PD       0:00      1 (Dependency)
       52896226_20    shared estimate  mkandes  R       0:27      1 exp-1-29
       52896226_19    shared estimate  mkandes  R       0:28      1 exp-1-29
       52896226_16    shared estimate  mkandes  R       0:29      1 exp-1-38
       52896226_17    shared estimate  mkandes  R       0:29      1 exp-1-38
       52896226_18    shared estimate  mkandes  R       0:29      1 exp-1-29
       52896226_14    shared estimate  mkandes  R       0:30      1 exp-1-29
       52896226_15    shared estimate  mkandes  R       0:30      1 exp-1-29
       52896226_11    shared estimate  mkandes  R       0:31      1 exp-1-29
       52896226_12    shared estimate  mkandes  R       0:31      1 exp-1-38
       52896226_13    shared estimate  mkandes  R       0:31      1 exp-1-38
[mkandes@login02 scripts]$
```

Check the summary statistics once the job completes. 

*Command*
```
cat compute-pi-stats.o*
```

*Output*
```
[mkandes@login02 scripts]$ ls
compute-pi-stats.o52896252.exp-1-08  estimate-pi.o52896226.14.exp-1-29  estimate-pi.o52896226.1.exp-1-29   estimate-pi.o52896226.6.exp-1-29
compute-pi-stats.sh                  estimate-pi.o52896226.15.exp-1-29  estimate-pi.o52896226.20.exp-1-29  estimate-pi.o52896226.7.exp-1-29
estimate-pi.o52896226.10.exp-1-29    estimate-pi.o52896226.16.exp-1-38  estimate-pi.o52896226.2.exp-1-29   estimate-pi.o52896226.8.exp-1-29
estimate-pi.o52896226.11.exp-1-29    estimate-pi.o52896226.17.exp-1-38  estimate-pi.o52896226.3.exp-1-29   estimate-pi.o52896226.9.exp-1-29
estimate-pi.o52896226.12.exp-1-38    estimate-pi.o52896226.18.exp-1-29  estimate-pi.o52896226.4.exp-1-29   estimate-pi.sh
estimate-pi.o52896226.13.exp-1-38    estimate-pi.o52896226.19.exp-1-29  estimate-pi.o52896226.5.exp-1-29   pi-workflow.sh
[mkandes@login02 scripts]$ cat compute-pi-stats.o*
Resetting modules to system default. Reseting $MODULEPATH back to system default. All extra directories will be removed from $MODULEPATH.

* FILE: 
  Records:           20
  Out of range:       0
  Invalid:            0
  Header records:     0
  Blank:              0
  Data Blocks:        1

* COLUMN: 
  Mean:               3.1417
  Std Dev:            0.0002
  Sample StdDev:      0.0002
  Skewness:          -0.1008
  Kurtosis:           2.5628
  Avg Dev:            0.0001
  Sum:               62.8330
  Sum Sq.:          197.3993

  Mean Err.:          0.0000
  Std Dev Err.:       0.0000
  Skewness Err.:      0.5477
  Kurtosis Err.:      1.0954

  Minimum:            3.1413 [17]
  Maximum:            3.1420 [19]
  Quartile:           3.1416 
  Median:             3.1416 
  Quartile:           3.1417 

3.1416500494165 0.000188386885705403
[mkandes@login02 scripts]$
```

### Pi-peline it: Creating a simple workflow

Finally, download the following batch job script. It recreates the simple workflow we ran above manually in a single batch job. Workflow jobs like this can be used to write (and launch) more complex job dependencies than you might do so directly from the command-line.

```
wget https://raw.githubusercontent.com/sdsc/sdsc-summer-institute-2025/refs/heads/main/3.2_high_throughput_computing/run-pi-workflow.sh
```

Once you've downloaded the script, go ahead and launch the workflow. 

```
[xdtr108@login02 ~]$ sbatch run-pi-workflow.sh 
Submitted batch job 14807605
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          14807605    shared run-pi-w  xdtr108  R       0:02      1 exp-1-06
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
       14807628_20    shared estimate  xdtr108 PD       0:00      1 (JobArrayTaskLimit)
       14807628_19    shared estimate  xdtr108 PD       0:00      1 (JobArrayTaskLimit)
       14807628_18    shared estimate  xdtr108 PD       0:00      1 (JobArrayTaskLimit)
       ...
        14807628_8    shared estimate  xdtr108  R       0:41      1 exp-1-12
        14807628_9    shared estimate  xdtr108  R       0:41      1 exp-1-27
       14807628_10    shared estimate  xdtr108  R       0:41      1 exp-1-27
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          14807629    shared compute-  xdtr108 PD       0:00      1 (Dependency)
       14807628_11    shared estimate  xdtr108  R       0:15      1 exp-1-06
       ...
       14807628_19    shared estimate  xdtr108  R       0:15      1 exp-1-08
       14807628_20    shared estimate  xdtr108  R       0:15      1 exp-1-08
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          14807629    shared compute-  xdtr108 PD       0:00      1 (Dependency)
       14807628_11    shared estimate  xdtr108  R       0:58      1 exp-1-06
       ...
       14807628_18    shared estimate  xdtr108  R       0:58      1 exp-1-08
       14807628_20    shared estimate  xdtr108  R       0:58      1 exp-1-08
[xdtr108@login02 ~]$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
[xdtr108@login02 ~]$ ls
4pi                                  estimate-pi.o14807628.10.exp-1-27
compute-pi-stats.o14806656.exp-1-08  estimate-pi.o14807628.11.exp-1-06
compute-pi-stats.o14807629.exp-1-06  estimate-pi.o14807628.12.exp-1-06
compute-pi-stats.sh                  estimate-pi.o14807628.13.exp-1-06
estimate-pi.o14806584.10.exp-1-08    estimate-pi.o14807628.14.exp-1-06
estimate-pi.o14806584.11.exp-1-08    estimate-pi.o14807628.15.exp-1-06
...
estimate-pi.o14806584.5.exp-1-08     estimate-pi.o14807628.9.exp-1-27
estimate-pi.o14806584.6.exp-1-08     estimate-pi.sh
estimate-pi.o14806584.7.exp-1-08     run-pi-workflow.o14807605.exp-1-06
estimate-pi.o14806584.8.exp-1-08     run-pi-workflow.sh
estimate-pi.o14806584.9.exp-1-08
[xdtr108@login02 ~]$
```

#

Next - [Batch job bundling](bundling.md)
