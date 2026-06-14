[← Back to all guides](../../../README.md)

# 01 — Getting Started: Running JDeveloper SOA Suite Quick Start 12c with Docker

A guide to run Oracle JDeveloper SOA Quick Start 12.2.1.4 using Docker, with a customized image based on Oracle JDK 8 and Oracle Linux 8.

> 📌 Credit: This guide is based on [damasiormoura/soasuitequickstart_docker_image](https://github.com/damasiormoura/soasuitequickstart_docker_image), modified to use Oracle JDK 8 (`oraclelinux8`) as the base image instead of the original.

---

## Prerequisites

- Windows laptop
- VMware Ubuntu 24.04.4 LTS desktop with [Docker](https://docs.docker.com/engine/install/ubuntu/) and internet access.
- [MobaXterm](https://mobaxterm.mobatek.net/) to access the Ubuntu VM from Windows
- A free [Oracle account](https://profile.oracle.com/myprofile/account/create-account.jspx) to accept image licenses
- [Oracle SOA Suite Quick Start](https://www.oracle.com/ae/middleware/technologies/soasuite/downloads.html) installation zip files:
  - `V983385-01_1of2.zip`
  - `V983385-01_2of2.zip`

---

## Step 1 — Accept the JDK License and Pull the Image

Before pulling, accept the Oracle JDK license at:
🔗 [https://container-registry.oracle.com/ords/ocr/ba/java/jdk](https://container-registry.oracle.com/ords/ocr/ba/java/jdk)

Then login and pull the image:

```bash
docker login container-registry.oracle.com
docker pull container-registry.oracle.com/java/jdk:8u491-oraclelinux8
```

> ⚠️ Skipping the license acceptance will cause the pull to fail with an authorization error.

---

## Step 2 — Clone This Repository

```bash
git clone https://github.com/ahfarag/oracle-fusion-middleware.git
cd oracle-fusion-middleware/soa-suite/12c/01-getting-started
```
---

## Step 3 — Add the SOA Suite Installation Files

You need to add the **installation JAR files**, which cannot be redistributed and must be downloaded separately. Unzip the SOA Suite Quick Start zip files and place the extracted JARs into the `install` folder:

```bash
cd install
```

The build expects:
- `fmw_12.2.1.4.0_soa_quickstart.jar`
- `fmw_12.2.1.4.0_soa_quickstart2.jar`


> 💡 A `patches/` folder is included with a `.gitkeep` file to maintain compatibility with the original repo structure. It is not used in this guide — if you need to apply SOA patches, refer to the [original repo](https://github.com/damasiormoura/soasuitequickstart_docker_image) for details.

---

## Step 4 — Build the Docker Image

From the `01-getting-started` folder:

```bash
docker build -t soaquickstart:12.2.1.4 .
```

> ⏳ This step takes several minutes as it installs JDeveloper and SOA Suite inside the image.

---

## Step 5 — Create the JDeveloper Working Directory

```bash
mkdir .jdeveloper
```

This directory will be mounted into the container to persist your JDeveloper workspace across runs.

---

## Step 6 — Run the Container

```bash
docker run --name soa-qs-12c -ti \
  --env DISPLAY=<YOUR_MOBAXTERM_IP>:0.0 \
  -p 7101:7101 \
  -v $(pwd)/.jdeveloper:/u01/oracle/.jdeveloper \
  soaquickstart:12.2.1.4
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

## Step 8 — Access the Server Console

Use the **Ubuntu VM's IP address** with port `7101` to access the console from your Windows browser:

```
http://<UBUNTU_VM_IP>:7101/console
```

---

## Troubleshooting

### Service Bus Console Fails with IPv6 LDAP Error

If opening the Service Bus console fails and throws an error like in the logs:

```
Caused by: java.net.URISyntaxException: Malformed IPv6 address at index 8: ldap://[172.17.0.2]:7101
```

**Fix:** Add the following lines to `setUserOverrides.sh` and restart the Integrated Server:

```bash
vi $(pwd)/.jdeveloper/system12.2.1.4.42.190911.2248/DefaultDomain/bin/setUserOverrides.sh
```

Add these lines:

```bash
#!/bin/sh

echo "*****************************************************"
echo "** Setting up UserOverrides.sh"

export EXTRA_JAVA_PROPERTIES="${EXTRA_JAVA_PROPERTIES} -Dcom.sun.jndi.ldapURLParsing=legacy"
export EXTRA_JAVA_PROPERTIES="${EXTRA_JAVA_PROPERTIES} -Dcom.sun.jndi.dnsURLParsing=legacy"
export EXTRA_JAVA_PROPERTIES="${EXTRA_JAVA_PROPERTIES} -Dcom.sun.jndi.rmiURLParsing=legacy"

echo EXTRA_JAVA_PROPERTIES=${EXTRA_JAVA_PROPERTIES}
echo "."
echo "."

echo "*****************************************************"
echo "** End UserOverrides.sh setup"
echo "*****************************************************"
```

Save the file, then restart the Integrated Server from JDeveloper.

---

## Verify

After the fix, log into the Service Bus console `http://<UBUNTU_VM_IP>:7101/servicebus` and confirm it loads without errors.

---

## References

- [damasiormoura/soasuitequickstart_docker_image](https://github.com/damasiormoura/soasuitequickstart_docker_image)
- [Oracle Container Registry — JDK](https://container-registry.oracle.com/ords/ocr/ba/java/jdk)
- [Oracle SOA Suite 12c Documentation](https://docs.oracle.com/en/middleware/soa-suite/soa/12.2.1.4/)
