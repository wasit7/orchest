import docker
import os
import uuid

def run_orchest_ctl(client, command):

    return client.containers.run("orchestsoftware/orchest-ctl:latest", command, name='orchest-ctl-' + str(uuid.uuid4()), detach=True, auto_remove=True,
        mounts=[
            docker.types.Mount(source="/var/run/docker.sock", target="/var/run/docker.sock", type='bind'),
            docker.types.Mount(source=os.environ.get("HOST_REPO_DIR"), target="/orchest-host", type='bind')
        ],
        environment={
            "HOST_CONFIG_DIR": os.environ.get("HOST_CONFIG_DIR"),
            "HOST_REPO_DIR": os.environ.get("HOST_REPO_DIR"),
            "HOST_USER_DIR": os.environ.get("HOST_USER_DIR")
        }
    )