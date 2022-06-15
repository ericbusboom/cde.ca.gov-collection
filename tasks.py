from invoke import task, Collection
from pathlib import Path

from metapack_build.tasks.collection import ns, foreach_metapack_subdir, ns_foreach_task_subdir



@task
def git_add(c):
    """Run git commit -a  on all submodules"""
    c.run(f"git submodule foreach 'git add -A'")

ns.add_task(git_add)

@task
def update_files(c):
    """Print the package url for each sub directory"""
    
    for d in foreach_metapack_subdir(c):
        c.run('mp update -f -S')
        
ns.add_task(update_files)


@task
def update_license(c):
    """Update the license at the end of the README in each package with the
    contents of the license_template.txt file"""
    import re
    
    p = re.compile('\s+<!-- start_license -->(.*)<!-- end_license -->', re.M|re.DOTALL)
    
    lictxt = "\n\n"+Path('./license-template.txt').read_text()
    
    for d in foreach_metapack_subdir(c):
 
        readme_file = Path('README.md')
        try:
            readme = readme_file.read_text()
            
            if '<!-- start_license -->' in readme:
                print('Replacing')
                readme_file.write_text( p.sub(lictxt, readme))
            else:
                print("Adding")
                readme_file.write_text(readme+lictxt)
        except FileNotFoundError:
            pass
    
        
ns.add_task(update_license)

# This is an example task for iterating over all of the sub directoryies
# that have a data package ( directory with metadata.csv ) Th
# foreach_metapack_subdir generator returns pathlib.Path() for each directory
# and changes the current directory into that directory. 
@task
def foreach_package(c):
    """Print the package url for each sub directory"""
    
    for d in foreach_metapack_subdir(c):
        c.run('mp info -p')
        
ns.add_task(foreach_package)

# You can also iterate over all directories that are set up for
# invoke, with a tasks.py file. The ns_foreach_task_subdir returns the 
# Invoke Collection, which holds all of the tasks for the directory. The 
# generator also changes the current working directory each iteration. 
@task
def foreach_tasks(c):
    """Print invoke's configuration by running the config tasks in each subdirectory """
    for sp_ns in ns_foreach_task_subdir(c):
        try:
            sp_ns.tasks.config(c)
        except UnexpectedExit:
            pass
            
ns.add_task(foreach_tasks)

