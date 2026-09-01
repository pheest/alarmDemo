#!../../bin/linux-x86_64/alarmDemo

#- SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#-
#- SPDX-License-Identifier: EPICS

#- You may have to change alarmDemo to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/alarmDemo.dbd"
alarmDemo_registerRecordDeviceDriver pdbbase

py "import alarm"
py "alarm.build()"

## Load record instances
dbLoadRecords("db/alarm.db","P=")

cd "${TOP}/iocBoot/${IOC}"
iocInit

dbpf OUT_PINI:YES 5
