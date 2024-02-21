"""
Automates the update process for ERP integration scripts by pulling changes from a Git repository
and copying a specific PHP script to a Docker volume.

This script performs the following operations:
- Pulls the latest changes from a specified Git repository to a local directory.
- Copies a specific PHP script from the updated local directory to a Docker volume used by a WordPress Docker container.

Attributes:
    REPO (str): The URL of the Git repository containing the ERP integration scripts.
    ERP_INEGRATION_PARENT_FOLDER (str): The local directory path where the Git repository is cloned and updated.
    WP_DOCKER_VOLUME (str): The path to the Docker volume where the WordPress instance is hosted.
    ERP_SYNC_PHP_SCRIPT (str): The name of the PHP script that is copied to the Docker volume to update the ERP integration.

Requires:
    - The script assumes that the Git repository is already cloned in the specified local directory.
    - The Docker volume path must be correct and accessible from the script execution context.

Usage:
    Run this script to automatically update the ERP integration scripts for a WordPress site hosted in Docker. Ensure
    that environment variables and paths are correctly configured for your specific deployment environment.
"""

#!/usr/local/bin/python3
import os

REPO = "https://github.com/gillmoreno/af_erp_sync.git"
ERP_INEGRATION_PARENT_FOLDER = "/opt/af_erp_sync"
WP_DOCKER_VOLUME = "/var/lib/docker/volumes/wp_docker_ubuntu_app/_data"
ERP_SYNC_PHP_SCRIPT = "_erp_sync.php"

os.system(
    f"""
    echo ">>> Pulling from git repo" &&
    cd {ERP_INEGRATION_PARENT_FOLDER} &&
    git pull &&
    echo ">>> Copying php script to docker volume" &&
    cp {ERP_INEGRATION_PARENT_FOLDER}/{ERP_SYNC_PHP_SCRIPT} {WP_DOCKER_VOLUME}/{ERP_SYNC_PHP_SCRIPT} &&
    echo ">>> OKIDOUK Brody :-)"
"""
)
