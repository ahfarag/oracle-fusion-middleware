#
# Based on https://github.com/damasiormoura/soasuitequickstart_docker_image
# Modified to use Oracle JDK 21 and soa suite 14c (container-registry.oracle.com/java/jdk:21.0.11-oraclelinux9)
# and Oracle Linux 9 as the base image.
#
# ORACLE DOCKERFILES PROJECT
# --------------------------
# This is the Dockerfile for Oracle SOA Suite Quick Start
#
# REQUIRED FILES TO BUILD THIS IMAGE
# ----------------------------------
# See soasuite.download file in the install directory
# Also see soapatches.download file in the patches directory
#

# Pull base image
# ---------------
FROM container-registry.oracle.com/java/jdk:21.0.11-oraclelinux9 AS builder

# Maintainer
# ----------
LABEL maintainer="Rodrigo Moura <rodrigo.moura@gmail.com>"

# Common environment variables required for this build
# ----------------------------------------------------
ENV ORACLE_HOME=/u01/oracle \
    USER_MEM_ARGS="-Djava.security.egd=file:/dev/./urandom" \
    PATH=$PATH:${JAVA_HOME}/bin:/u01/oracle/oracle_common/common/bin:/u01/oracle/wlserver/common/bin

# Ensure that images are updated during the build process as advised by Oracle
RUN yum -y update && rm -rf /var/cache/yum 

# Setup subdirectory for FMW install package and container-dummy.sh
# -----------------------------------------------------------------
RUN mkdir -p /u01 && \
    chmod a+xr /u01 && \
    useradd -b /u01 -d /u01/oracle -m -s /bin/bash oracle

#
# Environment variables required for this build (do NOT change)
# -------------------------------------------------------------
USER root
ENV FMW_JAR=fmw_14.1.2.0.0_soa_quickstart.jar

#
# Copy installers and patches for install
# -------------------------------------------
ADD install/* /u01/
RUN mkdir /u01/patches && \
    chown oracle:oracle -R /u01
COPY patches/* /u01/patches/
COPY container-scripts/* /u01/oracle/container-scripts/
RUN  cd /u01 && chmod 755 *.jar && \
     chmod +xr /u01/oracle/container-scripts/*.*

#
# Install
# -----------------------------------
USER oracle
RUN cd /u01 && \
  $JAVA_HOME/bin/java -jar $FMW_JAR -silent -responseFile /u01/soasuite.response -invPtrLoc /u01/oraInst.loc -jreLoc $JAVA_HOME -ignoreSysPrereqs -force -novalidation ORACLE_HOME=$ORACLE_HOME

#
# Apply SOA Patches
# -----------------
RUN patchzips=`ls /u01/patches/p*.zip 2>/dev/null`; \
    if [ ! -z "$patchzips" ]; then \
      cd /u01/patches;  \
      echo -e "\nBelow patches present in patches directory. Applying these patches:"; \
      ls p*.zip; \
      echo -e ""; \
      for filename in `ls p*.zip`; do echo "Extracting patch: ${filename}"; $JAVA_HOME/bin/jar xf ${filename}; done; \
      rm -f /u01/patches/p*.zip; \
      $ORACLE_HOME/OPatch/opatch napply -silent -oh $ORACLE_HOME -jre $JAVA_HOME -invPtrLoc /u01/oraInst.loc -phBaseDir /u01/patches; \
      $ORACLE_HOME/OPatch/opatch util cleanup -silent; \
      rm -rf /u01/patches /u01/oracle/cfgtoollogs/opatch/*; \
      echo -e "\nPatches applied in SOA oracle home are:"; \
      cd $ORACLE_HOME/OPatch; \
      $ORACLE_HOME/OPatch/opatch lspatches; \
    else \
      echo -e "\nNo patches present in patches directory. Skipping patch application."; \
    fi

#
# Rebuild from base image
# -----------------------
FROM container-registry.oracle.com/java/jdk:21.0.11-oraclelinux9

# Maintainer
# ----------
LABEL maintainer="Rodrigo Moura <rodrigo.moura@gmail.com>"

# Common environment variables required for this build
# ----------------------------------------------------
ENV ORACLE_HOME=/u01/oracle \
    M2_HOME=/u01/oracle/oracle_common/modules/thirdparty/apache-maven_bundle/3.9.4.0.0/apache-maven-3.9.4 \
    USER_MEM_ARGS="-Djava.security.egd=file:/dev/./urandom" \
    WL_HOME=/u01/oracle/wlserver \
    PATH=$PATH:/u01/oracle/oracle_common/common/bin:/u01/oracle/wlserver/common/bin

ENV PATH=${JAVA_HOME}/bin:${M2_HOME}/bin:$PATH


# Ensure that images are updated during the build process as advised by Oracle
RUN yum -y update && rm -rf /var/cache/yum 

# Setup subdirectory for FMW install package and container-dummy.sh
# -----------------------------------------------------------------
RUN mkdir -p /u01 && \
    chmod a+xr /u01 && \
    useradd -b /u01 -d /u01/oracle -m -s /bin/bash oracle

COPY --from=builder --chown=oracle:oracle /u01/oracle /u01/oracle

#
# Install the required packages
# -----------------------------
USER root

# The minimal packages required to fix the Java error and render the GUI
# java.lang.UnsatisfiedLinkError: /usr/java/jdk-21/lib/libawt_xawt.so: 
#    libXext.so.6: cannot open shared object file: No such file
RUN dnf install -y libXext libXrender libXi libXtst && \
    dnf clean all

#
# Define default command to start JDeveloper
#
USER oracle
WORKDIR $ORACLE_HOME
CMD ["/u01/oracle/jdeveloper/jdev/bin/jdev"]
