Profiling exercise
==================

We will run all the examples on a worker node.
Start an interactive session with
srun --partition=shared --reservation=si26cpu --account=sdp173 --pty --nodes=1 --ntasks-per-node=1 --mem=72G -c 32 -t 00:30:00 /bin/bash
(Adapt partition/reservation/account if needed)

Build a real application
------------------------

We will profile a real application, namely bowtie2, a popular bioinformatics short aligner.

The source files are available on github (github.com/BenLangmead/bowtie2/), but we also have them pre-staged on Expanse:
################
tar -xzf /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/source/v2.5.0.tar.gz 

# build
#######
module load gcc/10.2.0
cd bowtie2-2.5.0
make -j

Check that the binary works
---------------------------

We need a file containing a set of short reads, and a reference database.
We have the prestaged, but you can get them from https://ftp.microbio.me/pub/wol2/databases/bowtie2/ and qiita 101636.

Bowtie2 can be run many ways, but
we will use this specific command (should take about a minute):
#################################
rm -f out.sam; /bin/time ./bowtie2-align-l --wrapper basic-0 -p 31 -k 16 --seed 42 --very-sensitive --np 1 --mp 1,1 --rdg 0,1 --rfg 0,1 --score-min L,0,-0.05 --no-head --no-exact-upfront --no-1mm-upfront -x /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/db/WoLr2 -q /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/input/Mousseau88_FIN_373_host_filtered_quarter.fastq.gz >out.sam

Sampling profiling
------------------

An easy way to get an idea of where most of the time is spent, is to use the 
perf
sampling profiler:

First, you collect the data (no changes to the binary needed): 
###########################
rm perf.data out.sam; /bin/time perf record -F 25 -g -- ./bowtie2-align-l --wrapper basic-0 -p 31 -k 16 --seed 42 --very-sensitive --np 1 --mp 1,1 --rdg 0,1 --rfg 0,1 --score-min L,0,-0.05 --no-head --no-exact-upfront --no-1mm-upfront -x /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/db/WoLr2 -q /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/input/Mousseau88_FIN_373_host_filtered_quarter.fastq.gz >out.sam

You can safely ignore the warnings.
Did the runtime change significantly?

Next, you display the collected metrics:
#######################################
perf report -U

or
perf report -U > report_ms.txt

Can you spot any obvious places where the code is spending its time?


Check a different input file
----------------------------

Let's check a different input file:
##################################
rm perf.data out.sam; /bin/time perf record -F 25 -g -- ./bowtie2-align-l --wrapper basic-0 -p 31 -k 16 --seed 42 --very-sensitive --np 1 --mp 1,1 --rdg 0,1 --rfg 0,1 --score-min L,0,-0.05 --no-head --no-exact-upfront --no-1mm-upfront -x /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/db/WoLr2 -q /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/input/Song53_24613_host_filtered.fastq.gz >out.sam

This will run significantly longer (about 3 minutes)
You may want to try to undersatnd the source code while you wait.

When you check the report, is the code still spending its time in the same place
=========================
perf report -U > report_sg.txt


Attach to a running process
---------------------------

Profiling multi-process applications (e.g. MPI) is often much more challenging.
One way to make the process easier, is to separate process launching from actual profiling.

Of course, the same approach can be used for single-process applications, too.

So, let's start bowtie2 without perf, and put it in the background
##################################################################
rm perf.data out.sam; ./bowtie2-align-l --wrapper basic-0 -p 31 -k 16 --seed 42 --very-sensitive --np 1 --mp 1,1 --rdg 0,1 --rfg 0,1 --score-min L,0,-0.05 --no-head --no-exact-upfront --no-1mm-upfront -x /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/db/WoLr2 -q /expanse/lustre/projects/sdp173/sfiligoi/bowtie2/input/Song53_24613_host_filtered.fastq.gz >out.sam &

The immediate output will be the PID of the process.

Use that PID to attach perf to the running process:
##############################
perf record -F 25 -g -p <PID>

This will block, until the profiled process terminates.
(You can also just terminate prof without affecting bowtie2)

Use report, like before, to interpret the collected data.

