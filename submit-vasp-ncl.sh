#!/bin/bash


#SBATCH --partition=shared
#SBATCH --job-name="PEA_SoC_4x4x1"
#SBATCH --nodes=6-20
#SBATCH --exclusive
#SBATCH --time=07-00:00:00
#SBATCH --constraint=[op]
#SBATCH --exclude=node35,node36,node40,node02


module load vasp/5.4.4-intel2017a-wannier



# # set MPI executable
MPI_EXEC=$(which mpirun)



# # set application executable
VASP_BIN=$(which vasp_ncl)
ulimit -s unlimited
export NTASKS=$[$SLURM_CPUS_ON_NODE*$SLURM_JOB_NUM_NODES]



#a sed command to edit as necessary
sed -i  '/NCORE/s/.*/NCORE =  '"$SLURM_CPUS_ON_NODE"'/' INCAR
$MPI_EXEC -np $NTASKS  $VASP_BIN
