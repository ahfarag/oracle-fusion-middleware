[← Back to all guides](../../../README.md)

# 01 — Getting Started: Running JDeveloper SOA Suite Quick Start 14c with Docker

A guide to run Oracle JDeveloper SOA Quick Start 14.1.2.0.0 using Docker, with a customized image based on Oracle JDK 8 and Oracle Linux 8.

> 📌 Credit: This guide is based on [damasiormoura/soasuitequickstart_docker_image](https://github.com/damasiormoura/soasuitequickstart_docker_image), modified to use the JDeveloper SOA Quick Start 14.1.2.0.0.

---

## Prerequisites

- Windows laptop
- VMware Ubuntu 24.04.4 LTS desktop with [Docker](https://docs.docker.com/engine/install/ubuntu/) and internet access.
- [MobaXterm](https://mobaxterm.mobatek.net/) to access the Ubuntu VM from Windows
- A free [Oracle account](https://profile.oracle.com/myprofile/account/create-account.jspx) to accept image licenses
- [Oracle SOA Suite Quick Start](https://www.oracle.com/ae/middleware/technologies/soasuite/downloads.html) installation zip file `V1045350-01.zip`.

---

## Step 1 — Accept the JDK License and Pull the Image

Before pulling, accept the Oracle JDK license at:
🔗 [https://container-registry.oracle.com/ords/ocr/ba/java/jdk](https://container-registry.oracle.com/ords/ocr/ba/java/jdk)

Then login and pull the image:

```bash
docker login container-registry.oracle.com
docker pull container-registry.oracle.com/java/jdk:21.0.11-oraclelinux9
```

> ⚠️ Skipping the license acceptance will cause the pull to fail with an authorization error.

---

## Step 2 — Clone This Repository

```bash
git clone https://github.com/ahfarag/oracle-fusion-middleware.git
cd oracle-fusion-middleware/soa-suite/14c/01-getting-started
```
---

## Step 3 — Add the SOA Suite Installation Files

You need to add the **installation JAR files**, which cannot be redistributed and must be downloaded separately. Unzip the SOA Suite Quick Start zip files and place the extracted JARs into the `install` folder:

```bash
cd install
```

The build expects:
- `fmw_14.1.2.0.0_soa_quickstart.jar`


> 💡 A `patches/` folder is included with a `.gitkeep` file to maintain compatibility with the original repo structure. It is not used in this guide — if you need to apply SOA patches, refer to the [original repo](https://github.com/damasiormoura/soasuitequickstart_docker_image) for details.

---

## Step 4 — Build the Docker Image

From the `01-getting-started` folder:

```bash
docker build -t soa_qs:14.1.2 .
```

> ⏳ This step takes several minutes as it installs JDeveloper and SOA Suite inside the image.

---

## Step 5 — Create the JDeveloper Working Directory

```bash
MNT_LOC=<prefered mount location>
mkdir -p $MNT_LOC/jdeveloper/mywork $MNT_LOC/.jdeveloper
```

This directory will be mounted into the container to persist your JDeveloper workspace across runs.

---

## Step 6 — Run the Container

```bash
docker run --name soa-qs-14c -ti \
  --env DISPLAY=<YOUR_MOBAXTERM_IP>:0.0 \
  -p 7101:7101 \
  -v $MNT_LOC/.jdeveloper:/u01/oracle/.jdeveloper \
  -v $MNT_LOC/jdeveloper/mywork:/u01/oracle/jdeveloper/mywork \
  soa_qs:14.1.2
```

Replace `<YOUR_MOBAXTERM_IP>` with the IP shown when you hover over the **X server** icon in the top-right corner of the MobaXterm window.

When prompted, click **Yes** to allow UI export over the display.

---

## Step 7 — Start the Integrated Server

Inside JDeveloper:

1. Start the **Integrated WebLogic Server**
2. Enter the admin password when prompted
3. Wait for the installation and startup to complete

> 💡 If you need a different port than `7101`, update the `-p` flag in the `docker run` command accordingly.

---

## Step 8 — Access the Remote Weblogic Console

The original administration console is no longer supported in WebLogic Server 14.1.2.0.0 and has been removed.

Deploy Hosted WebLogic Remote Console:

```bash
docker exec -it soa-qs-14c /bin/bash
echo "<WeblogicPassword>" > $HOME/password.txt
$ORACLE_HOME/oracle_common/common/bin/wlst.sh $WL_HOME/server/bin/remote_console_deployment.py t3://localhost:7101 weblogic < $HOME/password.txt
```

Use the **Ubuntu VM's IP address** with port `7101` to access the remote console from your browser:

```
http://<UBUNTU_VM_IP>:7101/rconsole
```

---

## Verify

After the fix, log into the Service Bus console `http://<UBUNTU_VM_IP>:7101/servicebus` and confirm it loads without errors.

---

## References

- [damasiormoura/soasuitequickstart_docker_image](https://github.com/damasiormoura/soasuitequickstart_docker_image)
- [Oracle Container Registry — JDK](https://container-registry.oracle.com/ords/ocr/ba/java/jdk)
- [Oracle SOA Suite 14c Documentation](https://docs.oracle.com/en/middleware/soa-suite/soa/14.1.2/index.html)
- [More about silent installation](https://docs.oracle.com/en/middleware/fusion-middleware/12.2.1.4/ouirf/using-oracle-universal-installer-silent-mode.html#OUIRF323)
- [Maven Based Build and Deploy](https://docs.oracle.com/en/middleware/soa-suite/soa/14.1.2/soakn/maven-based-build-deploy.html)
- [Deploy Hosted WebLogic Remote Console](https://oracle.github.io/weblogic-remote-console/set-console/#GUID-9974090F-7983-4641-9121-36A29B6F6735)
