
import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', help="The version you want for the packages", default=None)
parser.add_argument('-n', '--notes', help="Release notes", default="")
parser.add_argument('-s', '--send_package', help="Shows you which apps and what actions it would have performed, doesn't actually do anything though", action='store_true', default=False)
args = parser.parse_args()

version = args.version
notes = args.notes
send_package = args.send_package

f = open("base.nuspec")
base_nuspec = f.read()
f.close()

items = os.listdir('.')

def dylib_name(folder_path):
    frameworks = os.path.join(folder_path,"Frameworks")
    if not os.path.exists(frameworks):
        return ""
    stuff = os.listdir(frameworks)
    for item in stuff:
        if item.endswith(".dylib"):
            return item
    return ""

for folder in items:
    if not os.path.isdir(folder):
        continue
    id = folder    
    if not folder.startswith("Xamarin.Swift4."):
        if folder == "Xamarin.Swift4":
            id = "Xamarin.Swift4.Support"
        else:
            continue
    
    lib = dylib_name(os.path.join(".",folder))
    nuspec = "%s.nuspec" % id
    package = "%s.%s.nupkg" % (folder,version)

    nuspec_content = base_nuspec
    nuspec_content = nuspec_content.replace("$id$",id)
    nuspec_content = nuspec_content.replace("$lib$",lib)
    nuspec_content = nuspec_content.replace("$version$",version)
    nuspec_content = nuspec_content.replace("$releaseNotes$",notes)

    f = open(os.path.join(folder,nuspec),"w")
    f.write(nuspec_content)
    f.close()

    cmd = subprocess.Popen(["nuget","pack",nuspec], cwd=folder)
    cmd.wait()

    # TODO: Make use of send_package
