#!/bin/sh
#SBATCH --partition=shared
#SBATCH --job-name="HOIP_Dataset"
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=06-23:59:59
#SBATCH --constraint=[ib|op]
#SBATCH -o slurm.out
#SBATCH -e slurm.err



module load anaconda3/2019.03
module load vasp/5.4.4-intel2017a-wannier



MPI_EXEC="/opt/eb-pkg/ebadmin/software/impi/2017.1.132-iccifort-2017.1.132-GCC-6.3.0-2.27/bin64/mpirun"
MPI_EXEC=$(which mpirun)



# # set application executable
VASP_BIN="/opt/proprietary-apps/vasp/5.4.4-intel-2017a-wannier/bin/vasp_std"
VASP_BIN=$(which vasp_std)
ulimit -s unlimited
#export NTASKS=$($SLURM_CPUS_ON_NODE*$SLURM_JOB_NUM_NODES)



## For old ase VASP connection use dis
#export VASP_COMMAND=$MPI_EXEC -np $NTASKS  $VASP_BIN



##For new ase VASP2 connection
#export ASE_VASP_COMMAND=$MPI_EXEC -np $NTASKS $VASP_BIN
##For new ase VASP2 connection
export ASE_VASP_COMMAND="/opt/eb-pkg/ebadmin/software/impi/2017.1.132-iccifort-2017.1.132-GCC-6.3.0-2.27/bin64/mpirun -np 16 /opt/proprietary-apps/vasp/5.4.4-intel-2017a-wannier/bin/vasp_std"
export VASP_PP_PATH="$HOME/VASP_Pseudopotentials"
export VASP_SCRIPT="$HOME/ASE/run_vasp.py"
source /users/cu0003/ASE_env/bin/activate
python3 ASE_A_Sites.py
