#a script to merge two eu4 mods 
#the user can select the diffs to keep when there are conflicts in the files

import sys
import zipfile
import difflib
import os
import diff_match_patch
import io
#closes the files and exits the program
def cleanup(rv):
    dest.close()
    s0.close()
    s1.close()
    exit(rv)
    
#generates the .mod file
def generate_mod_file(filename, merged_name, filepath):
    f = open(filepath, "w")
    f.write("name = \"" + 
            merged_name + 
        "\"\npath = \"mod/" + 
        filename + 
        "\"\nsupported_version = \"1.27.*.*\"\n")
    f.close()

if len(sys.argv) < 4:
    print("not enough arguments")
    print("usage:python eu4modmerger.py mod0.zip mod1.zip dest.zip")
    exit(0)
    
print("merging " + str(sys.argv[1]) + " with " + str(sys.argv[2]) + " to " +str(sys.argv[3]) )

#setup for .mod file
merged_name = os.path.basename(sys.argv[1]) + " " + os.path.basename(sys.argv[2])
merged_name = merged_name.replace(".zip", "")
mod_path = sys.argv[3].replace(".zip", ".mod")


dest = zipfile.ZipFile(sys.argv[3], 'w')
s0 = zipfile.ZipFile(sys.argv[1], 'r')
s1 = zipfile.ZipFile(sys.argv[2], 'r')

intersection = set(s0.namelist()) & set(s1.namelist())

    
s0ncf = set(s0.namelist()) - intersection
s1ncf = set(s1.namelist()) - intersection


#merge to unconflicting files
for i in s0ncf:
    #print(i)generate_mod_file(os.path.basename(sys.argv[3]), merged_name, mod_path)
    dest.writestr(i,s0.read(i))
for i in s1ncf:
    dest.writestr(i,s1.read(i))
    
if len(intersection) == 0:
    print("sucessful merge")
    generate_mod_file(os.path.basename(sys.argv[3]), merged_name, mod_path)
    cleanup(0)
    
#generate the diffs and then let the user select which to apply
dmp = diff_match_patch.diff_match_patch()
print("files with diffs:")
for i in intersection:
    print(i)
    s0file = s0.open(i)
    s1file = s1.open(i)
    s0string = s0file.read().decode("utf8")
    s1string = s1file.read().decode("utf8")
    s0file.close()
    s1file.close()
    
    
    patch = dmp.patch_make(s0string, s1string)
    patchtext = dmp.patch_toText(patch)
    #print(dmp.patch_toText(patch))
    correctedpatch = []
    for p in patch:
        print(p)
        print("use [y/N]")
        s = input()
        if s == "y":
            correctedpatch.append(p)
        elif s == "e":
            #kill without completing
            break
            continue
    
    
    patchedtext = dmp.patch_apply(correctedpatch, s0string)
    #convert the patched string to a file type
    pak = io.StringIO()
    pak.write(patchedtext[0])
    #print(patchedtext[0])
    dest.writestr(i, pak.getvalue())

    
generate_mod_file(os.path.basename(sys.argv[3]), merged_name, mod_path)
cleanup(0)
