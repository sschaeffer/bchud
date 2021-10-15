#!/usr/bin/bash

minecraftdir=/media/local/Minecraft
worldname=fury

MINECRAFTDIR=${1:-$minecraftdir}
WORLDNAME=${2:-$worldname}

BACKUPDATE=`date +'%Y-%m-%d_%H-%M-%S_'`
cd ${MINECRAFTDIR}/saves

zip -r "../backups/${BACKUPDATE}${WORLDNAME}.zip" "${WORLDNAME}"
