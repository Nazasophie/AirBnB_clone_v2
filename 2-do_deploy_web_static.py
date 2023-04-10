#!/usr/bin/python3
# Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers, using the function do_deploy

from fabric.api import *
import os

env.hosts = ['100.25.180.113', '34.203.75.86']

def do_deploy(archive_path):
    # Check if the archive file exists
    if not os.path.isfile(archive_path):
        print(f"Archive file '{archive_path}' does not exist!")
        return False

    try:
        # Upload archive to web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive filename without extension>
        filename = os.path.basename(archive_path)
        foldername = os.path.splitext(filename)[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(foldername))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, foldername))
        run('rm /tmp/{}'.format(filename))
        
        # Delete the symbolic link /data/web_static/current from the web server
        run('sudo rm -f /data/web_static/current')
        
        # Create a new symbolic link to the new version of code
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(foldername))
        print("New version deployed!")
        return True
        
    except:
        print("Deployment failed!")
        return False

