## Prerequisites
As a starting point, please ensure that the default modules are loaded. To confirm, we can run the command `module list`. The output should be  

>    Currently Loaded Modules:
>    1) shared   2) cpu/0.17.3b (c)   3) slurm/expanse/23.02.7   4) sdsc/1.0   5) DefaultModules

If needed, run `module reset` to set the modules to default.

## Hands-on session 1: working with modules
We will run a few module commands to search and load the system-wide installed MATLAB software
1. Search with the module string to show how to load a particular MATLAB

       module spider matlab
       module spider matlab/2022b
       module spider matlab/2022b/lefe4oq

2. Load MATLAB 2022b from the **CPU** software stack

       module reset
       module list
       module load cpu matlab/2022b    # same as module load cpu/0.17.3b matlab/2022b/lefe4oq since cpu/0.17.3b is the default CPU stack
       module list
       module show matlab/2022b
   
3. Check if the path to the MATLAB executable is correctly set

       which matlab

## Hands-on session 2: working with Singularity containers
In the first part of this hands-on section, we will copy over a PyTorch example from the Expanse examples directory and run it. 
1. Copy over a PyTorch example from the Expanse examples directory

       cp -r /cm/shared/examples/sdsc/pytorch .
       cd pytorch
    
2. Submit job with sbatch

       sbatch -A sdp173 --cpus-per-task=8 --mem=16G run-pytorch-cpu-shared.sh
           
3. Check the output file

       cat pytorch-cpu-shared.*

In the second part of this hands-on section, we will build a Singularity image on Expanse. 
1. First, start an interactive session

       srun --pty --partition=shared --nodes=1 --ntasks-per-node=1 --cpus-per-task=8 --mem=16G -A sdp173 -t 01:30:00 --wait 0 /bin/bash

2. Load Singularity module

       module reset
       module load singularitypro

3. Build an image lolcow.sif from `docker://godlovedc/lolcow`

       singularity build lolcow.sif docker://godlovedc/lolcow

4. Run this image with `singularity exec`

       singularity exec lolcow.sif fortune
       singularity exec lolcow.sif cowsay hello
       singularity exec lolcow.sif sh -c 'fortune | cowsay'
  
## Hands-on session 3: working with Python
We first start an interactive session, if the interactive session started in Hands-on session 2 has ended.

    srun --pty --partition=shared --nodes=1 --ntasks-per-node=1 --cpus-per-task=8 --mem=16G -A sdp173 -t 01:30:00 --wait 0 /bin/bash

Install Miniforge3 and then pyjokes 

1. Download and install miniforge3, make it available by alias

        wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
        bash Miniforge3-Linux-x86_64.sh -b -s
        alias miniforge='eval "$($HOME/miniforge3/bin/conda shell.bash hook)"' # alias can be added to ~/.bashrc
        miniforge 

2. Create and activate a conda environment 

        mamba create -n pyjokes
        conda activate pyjokes
   
3. Install pyjokes and run it

        mamba install pyjokes
        pyjokes


## Hands-on session 4: install from source

This example compiles cmatrix from source.

We first start an interactive session, if the interactive session started in Hands-on session 2 or 3 has ended.

    srun --pty --partition=shared --nodes=1 --ntasks-per-node=1 --cpus-per-task=8 --mem=16G -A sdp173 -t 01:30:00 --wait 0 /bin/bash

1. Set up module environment.  
   The ncurses module is available only in the cpu/0.15.4 software stack, so this example explicitly loads that stack instead of the current default cpu/0.17.3. 

       module reset
       module load cpu/0.15.4 gcc/10.2.0  ncurses/6.2

2. Build from source

       git clone https://github.com/abishekvashok/cmatrix
       cd cmatrix
       autoreconf -i
       ./configure --prefix=$HOME/cmatrix/install LIBS="-lncursesw"
       make
       make install

3. Add the bin path to PATH

       export PATH=$HOME/cmatrix/install/bin:$PATH

4. Run executable `cmatrix`

       cmatrix
