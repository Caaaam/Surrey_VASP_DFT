import os
import ase
import subprocess
import time
from ase.build import bulk
from ase.calculators.vasp import Vasp2
from ase.dft.bandgap import bandgap

def VASP_Relaxation(POSCAR):

    #print('test')
    os.system('mkdir ' + 'Folder_' + str(POSCAR))
    os.system('source ~/sumo_cam/bin/activate')

    os.system('rm WAVECAR; rm CHG; rm CHGCAR')

    # FIND WAY TO READ POSCAR
    Perovskite = ase.io.read(POSCAR, format = "vasp")

    # Calculator for relaxation
    calc = Vasp2(xc = 'vdw-df2',
                kspacing=0.2,
                prec = 'Accurate',
                ediff = 1*10**-4,
                ismear = 0,
                sigma = 0.01,
                ediffg = 1*10**-2,
                ibrion = 1,
                nsw = 100,
                isif = 3,
                encut = 400,
                gga = 'ML',
                luse_vdw = True,
                zab_vdw = -1.8867,
                aggac = 0.000,
                lasph = True)

    Perovskite.calc = calc

    Perovskite.get_potential_energy()  # Run the calculation

    os.system ('cp OUTCAR ' + 'Folder_' + str(POSCAR))
    os.system('cp CONTCAR ' + 'Folder_' +  str(POSCAR) + '/CONTCAR_' + str(POSCAR))
    os.system('cp CONTCAR ../CONTCAR_' + str(POSCAR))

    calc = Vasp2(xc = 'vdw-df2',
                kspacing=0.2,
                prec = 'Accurate',
                ediff = 1*10**-4,
                ismear = 0,
                sigma = 0.01,
                ediffg = 1*10**-2,
                ibrion = -1,
                nsw = 0,
                encut = 400,
                gga = 'ML',
                luse_vdw = True,
                zab_vdw = -1.8867,
                aggac = 0.000,
                lasph = True)

    Perovskite.calc = calc

    Perovskite.get_potential_energy()  # Run the calculation

    kptsband = {'path': 'GMRXGR', 'npoints': 100}     # Number of points along the path

    calc = Vasp2(xc = 'vdw-df2',
                kpts=kptsband,
                prec = 'Accurate',
                ediff = 1*10**-4,
                ismear = 0,
                sigma = 0.01,
                ediffg = 1*10**-2,
                ibrion = -1,
                nsw = 0,
                encut = 400,
                gga = 'ML',
                luse_vdw = True,
                zab_vdw = -1.8867,
                aggac = 0.000,
                lasph = True)

    Perovskite.calc = calc

    Total_Energy = Perovskite.get_potential_energy()  # Run the calculation

    gap, p1, p2 = bandgap(Perovskite.calc)

    os.system('cp vasprun.xml Folder_' + str(POSCAR))
    os.system('cp KPOINTS Folder_' + str(POSCAR))
    os.system('cd Folder_' + str(POSCAR))
    os.system("source ~/sumo_cam/bin/activate")
    os.system('sumo-bandstats')
    os.system('cp sumo-bandstats.log ../../bandstats_'+str(POSCAR))
    os.system('sumo-bandplot --ymin 0 --ymax 3 --dos vasprun.xml --format png')
    os.system('cp band.pdf ../../band_'+str(POSCAR)+'.png')
    os.system('cd ../')

    f = open('HOIP_Data2.txt', "a")
    f.write(f"{POSCAR}, {gap}, {Total_Energy}\n")
    f.close()

dir_name = os.getcwd()
#os.system('rm HOIP_Data2.txt')

# Finding all POSCAR's in directory
POSCARS = []
ext = 'POSCAR'

# iterating over all files
for files in os.listdir(dir_name):
    if files.startswith(ext):
        POSCARS.append(str(files))  # printing file name of desired extension
    else:
        continue

POSCARS.sort()

print(POSCARS)

for POSCAR in POSCARS:
    print(POSCAR)
    VASP_Relaxation(POSCAR)
    os.system(f"cp vasp.out vasp_{POSCAR}.out")
