#!/usr/local/bin/python3
import os

REPO = "https://github.com/gillmoreno/af_erp_sync.git"
ERP_INEGRATION_PARENT_FOLDER = "/opt/af_erp_sync"
WP_DOCKER_VOLUME = "/var/lib/docker/volumes/wp_docker_ubuntu_app/_data"
ERP_SYNC_PHP_SCRIPT = "_erp_sync.php"

os.system(f"""
    echo ">>> Pulling from git repo" &&
    cd {ERP_INEGRATION_PARENT_FOLDER} &&
    git pull &&
    echo ">>> Copying php script to docker volume" &&
    cp {ERP_INEGRATION_PARENT_FOLDER}/{ERP_SYNC_PHP_SCRIPT} {WP_DOCKER_VOLUME}/{ERP_SYNC_PHP_SCRIPT} &&
    echo ">>> OKIDOUK Brody :-)"
""")
