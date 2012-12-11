#---------------------------------------------------------------
# Project         : Mandrake Linux
# Module          : pvm
# File            : pvm.sh
# Author          : Erwan Velu
# Created On      : Wed Jan 04 17:25:58 2006
# Purpose         : Setting pvm env
#--------------------------------------------------------------
export PVM_RSH=/usr/bin/rsh
export PVM_ROOT=/usr/share/pvm3
export PVM_ARCH=`$PVM_ROOT/lib/pvmgetarch`
export PVMD_NOHOLD=ON
export PVM_TMP=/var/run/pvm3
export XPVM_ROOT=/usr/X11R6/lib/xpvm/
export PATH=$PATH:/usr/share/pvm3
