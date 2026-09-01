# SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#
# SPDX-License-Identifier: EPICS

TOP=../..

include $(TOP)/configure/CONFIG
include $(PYDEVSUP)/configure/CONFIG_PY
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = alarmDemo
# alarmDemo.dbd will be created and installed
DBD += alarmDemo.dbd

# alarmDemo.dbd will be made up from these files:
alarmDemo_DBD += base.dbd

# Include dbd files from all support applications:
alarmDemo_DBD += pyDevSup.dbd

# Add all the support libraries needed by this IOC
alarmDemo_LIBS += pyDevSup$(PY_LD_VER)

#USR_SYS_LIBS += python$(PY_LD_VER)

# alarmDemo_registerRecordDeviceDriver.cpp derives from alarmDemo.dbd
alarmDemo_SRCS += alarmDemo_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
alarmDemo_SRCS_DEFAULT += alarmDemoMain.cpp
alarmDemo_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#alarmDemo_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
alarmDemo_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
include $(PYDEVSUP)/configure/RULES_PY
#----------------------------------------
#  ADD RULES AFTER THIS LINE

