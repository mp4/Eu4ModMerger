#a script to merge two eu4 mods files in conflict will be marked using
#git tags for the two versions of the code

import sys
import zipfile
import difflib
import os
import diff_match_patch
import io

def cleanup(rv):
    dest.close()
    s0.close()
    s1.close()
    exit(rv)

if len(sys.argv) < 4:
    print("not enough arguments")
    exit(0)
    
print("merging " + str(sys.argv[1]) + " with " + str(sys.argv[2]) + " to " +str(sys.argv[3]) )

dest = zipfile.ZipFile(sys.argv[3], 'w')
s0 = zipfile.ZipFile(sys.argv[1], 'r')
s1 = zipfile.ZipFile(sys.argv[2], 'r')

intersection = set(s0.namelist()) & set(s1.namelist())

    
s0ncf = set(s0.namelist()) - intersection
s1ncf = set(s1.namelist()) - intersection


#merge to unconflicting files
for i in s0ncf:
    #print(i)
    dest.writestr(i,s0.read(i))
for i in s1ncf:
    dest.writestr(i,s1.read(i))
    
if len(intersection) == 0:
    print("sucessful merge")
    cleanup(0)
    

dmp = diff_match_patch.diff_match_patch()
print("files with diffs:")
for i in intersection:
    print(i)
    s0file = s0.open(i)
    s1file = s1.open(i)
    s0string = s0file.read().decode("utf8")#.splitlines(keepends=True)
    s1string = s1file.read().decode("utf8")#.splitlines(keepends=True)
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
    print(patchedtext[0])
    dest.writestr(i, pak.getvalue())

    
    

cleanup(0)
