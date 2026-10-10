#!../../bin/linux-x86_64/alarmDemo

#- SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#-
#- SPDX-License-Identifier: EPICS

#- You may have to change alarmDemo to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

epicsEnvSet("PINI", "${PINI='NO'}")
epicsEnvSet("RVAL", "${RVAL='VAL'}")
epicsEnvSet("HASH", "${HASH='#'}")

## Register all support components
dbLoadDatabase "dbd/alarmDemo.dbd"
alarmDemo_registerRecordDeviceDriver pdbbase

py "import alarm"
py "alarm.build()"

## Load record instances
dbLoadRecords("db/alarm.db","PINI=${PINI}, RVAL=${RVAL}, HASH=${HASH}")

cd "${TOP}/iocBoot/${IOC}"
iocInit
dbDumpRecord > dbDumpRecord.log
