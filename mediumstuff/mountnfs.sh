#!/bin/bash

EFS_REGION='us-east-1'
EFS_MOUNT_DIR='/efs'
EFS_VOLUME_ID='fs-dddddddd'
echo "Mounting EFS filesystem ${EFS_DNS_NAME} to directory ${EFS_MOUNT_DIR} ..."

echo 'Stopping NFS ID Mapper...'
service rpcidmapd status &> /dev/null
if [ $? -ne 0 ] ; then
    echo 'rpc.idmapd is already stopped!'
else
    service rpcidmapd stop
    if [ $? -ne 0 ] ; then
        echo 'ERROR: Failed to stop NFS ID Mapper!'
        exit 1
    fi
fi

echo 'Checking if EFS mount directory exists...'
if [ ! -d ${EFS_MOUNT_DIR} ]; then
    echo "Creating directory ${EFS_MOUNT_DIR} ..."
    mkdir -p ${EFS_MOUNT_DIR}
    if [ $? -ne 0 ]; then
        echo 'ERROR: Directory creation failed!'
        exit 1
    fi
    chmod 775 ${EFS_MOUNT_DIR}
    if [ $? -ne 0 ]; then
        echo 'ERROR: Permission update failed!'
        exit 1
    fi
else
    echo "Directory ${EFS_MOUNT_DIR} already exists!"
fi

mountpoint -q ${EFS_MOUNT_DIR}
if [ $? -ne 0 ]; then
    AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
    echo "mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 ${AZ}.${EFS_VOLUME_ID}.efs.${EFS_REGION}.amazonaws.com:/ ${EFS_MOUNT_DIR}"
    mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 ${AZ}.${EFS_VOLUME_ID}.efs.${EFS_REGION}.amazonaws.com:/ ${EFS_MOUNT_DIR}
    if [ $? -ne 0 ] ; then
        echo 'ERROR: Mount command failed!'
        exit 1
    fi
else
    echo "Directory ${EFS_MOUNT_DIR} is already a valid mountpoint!"
fi

echo 'EFS mount complete.'

