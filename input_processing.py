#!/usr/bin/env python3
import os
import argparse

def process_input(driver_input: str) -> str:
    summary = {}
    summary["directory"] = os.getcwd()
    # The rest of the script remains the same

    output = ""
    for key, value in summary.items():
        output += '#%s---%s\n' % (key, value)
    # The rest of the output generation remains the same

    return output

    summary={}
    summary["directory"]=os.getcwd()
    with open(args.driver_input,'r') as fo:
        lines = fo.readlines()
        for line in lines:
            if line[:len("PDB:")]=="PDB:":
                summary["PDB:"]=line.split("PDB:")[1].strip()
            elif line[:len("Seed:")]=="Seed:":
                summary["Seed:"]=line.split("Seed:")[1].strip()        
            elif line[:len("RIN_program:")]=="RIN_program:":
                summary["RIN_program:"]=line.split("RIN_program:")[1].strip()
            elif line[:len("Residue_to_add:")]=="Residue_to_add:":
                summary["Residue_to_add:"]=line.split("Residue_to_add:")[1].strip()
            elif line[:len("Histidine:")]=="Histidine:":
                summary["Histidine:"]=line.split("Histidine:")[1].strip()
            elif line[:len("Model(s):")]=="Model(s):":
                summary["Model(s):"]=line.split("Model(s):")[1].strip()
            elif line[:len("Substrate(s)_charge:")]=="Substrate(s)_charge:":
                summary["Substrate(s)_charge:"]=line.split("Substrate(s)_charge:")[1].strip()
            elif line[:len("Computational_program:")]=="Computational_program:":
                summary["Computational_program:"]=line.split("Computational_program:")[1].strip()
            elif line[:len("Multiplicity: ")]=="Multiplicity: ":
                summary["Multiplicity: "]=line.split("Multiplicity: ")[1].strip()                                                                          
            elif line[:len("residues_not_to_protonate:")]=="residues_not_to_protonate:":
                summary["residues_not_to_protonate:"]=line.split("residues_not_to_protonate:")[1].strip() 
            elif line[:len("seed_residues_want_to_freeze:")]=="seed_residues_want_to_freeze:":
                summary["seed_residues_want_to_freeze:"]=line.split("seed_residues_want_to_freeze:")[1].strip()                                                                          
    
    with open (f"output","w") as writestart:
        for key, value in summary.items(): 
            writestart.write('#%s---%s\n' % (key, value))
        writestart.write(f'\n\n#all script needs to run is here:\n\n#pymolscript will fail if pymol is set as alias and not in the export path in .bash_profilr or .bas_rc\n# it can be set up as adding "export PYMOLPATH=$HOME/pymol:$PYMOLPATH" in .bashprofile and source it')
        writestart.write(f'\n\n~/git/RINRUS/bin/reduce -NOFLIP {summary.get("PDB:").strip(".pdb")}.pdb > {summary.get("PDB:").strip(".pdb")}_h.pdb')
        writestart.write(f'\n~/git/RINRUS/bin/probe -MC -self "all" -unformated {summary.get("PDB:").strip(".pdb")}_h.pdb > {summary.get("PDB:").strip(".pdb")}_h.probe')
        writestart.write(f'\npython3 ~/git/RINRUS/bin/probe2rins.py -f {summary.get("PDB:").strip(".pdb")}_h.probe -s {summary.get("Seed:")}')
        writestart.write(f'\npython3 ~/git/RINRUS/bin/rinrus_trim2_pdb.py -s {summary.get("Seed:")} -pdb {summary.get("PDB:").strip(".pdb")}_h.pdb')

        writestart.write("\nls -lrt| grep -v slurm |awk '{print $9}'|grep -e .pdb |grep -e res| cut -d'_' -f2|cut -d'.' -f1>list; mkdir pdbs;")
        writestart.write('for i in `cat list`; do mkdir ${i}-01; cd ${i}-01; mv ../res_${i}* .;')
        writestart.write(f'python3 ~/git/RINRUS/bin/pymol_scripts.py -resids {summary.get("Seed:")} -pdbfilename *.pdb;')
        writestart.write('cp *_h.pdb model-${i}_h.pdb; cp model-${i}_h.pdb ../pdbs/; cp res_${i}_atom_info.dat ../pdbs/${i}.dat ; cd ..; done')
        writestart.write("\n\n#writeinput still needs to be generated ")
        
    print("all script needs to run is written in 'output' file")       
