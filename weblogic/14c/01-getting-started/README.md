[← Back to all guides](../../../README.md)

# 01 — Getting Started: Running Oracle WebLogic 14c with Docker

A quick-start guide to get Oracle WebLogic Server 14c (14.1.1.0) running locally using Docker — no manual installer, no JAVA_HOME headaches.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- An Oracle account (free) to accept the image license

---

## Step 1 — Accept the License

Before pulling the image, you must accept Oracle's license agreement through the Oracle Container Registry:

1. Go to: [https://container-registry.oracle.com/ords/ocr/ba/middleware/weblogic](https://container-registry.oracle.com/ords/ocr/ba/middleware/weblogic)
2. Sign in with your Oracle account
3. Click **Continue** to accept the license agreement for the WebLogic repository

> ⚠️ Skipping this step will cause the `docker pull` to fail with an authorization error.

---

## Step 2 — Login to the Oracle Container Registry

```bash
docker login container-registry.oracle.com
```

Enter your Oracle account credentials when prompted.

---

## Step 3 — Pull the WebLogic Image

```bash
docker pull container-registry.oracle.com/middleware/weblogic:14.1.1.0-dev-11-250425
```

This pulls the developer image of WebLogic 14.1.1.0 (JDK 11, April 2025 build).

---

## Step 4 — Create the Domain Properties File

WebLogic requires a properties file to configure the admin credentials at startup.

```bash
mkdir -p wls14c/properties && cd wls14c
```

Create the file `properties/domain.properties`:

```bash
vi properties/domain.properties
```

Add the following content:

```properties
username=weblogic
password=Welcome1
```

> 💡 You can change these credentials to anything you prefer. Just make sure the password meets WebLogic's complexity requirements (minimum 8 characters, at least one number).

---

## Step 5 — Start the WebLogic Container

From inside the `wls14c` directory:

```bash
docker run -it --rm \
  --name wls14c \
  -p 7001:7001 \
  -v $(pwd)/properties:/u01/oracle/properties \
  -e "ADMINISTRATION_PORT_ENABLED=false" \
  container-registry.oracle.com/middleware/weblogic:14.1.1.0-dev-11-250425
```

### What these flags do

| Flag | Description |
|---|---|
| `-it` | Interactive mode — lets you see server startup logs |
| `--rm` | Automatically removes the container when stopped |
| `--name wls14c` | Names the container for easy reference |
| `-p 7001:7001` | Maps the WebLogic HTTP port to your host |
| `-v $(pwd)/properties:/u01/oracle/properties` | Mounts the credentials file into the container |
| `-e "ADMINISTRATION_PORT_ENABLED=false"` | Disables the separate HTTPS admin port (simpler for local dev) |

Wait until you see the server running message like:

```
<Server state changed to RUNNING.>
```

---

## Step 6 — Access the Admin Console

Open your browser and navigate to:

```
http://localhost:7001/console
```

Log in with the credentials you set in `domain.properties` (`weblogic` / `Welcome1` by default).

---

## Configuration via Environment Variables

Many WebLogic domain settings can be customized at startup using environment variables passed via `-e`. The full list of supported variables is documented here:

🔗 [Oracle WebLogic Docker Images — Environment Variables Reference](https://github.com/oracle/docker-images/tree/main/OracleWebLogic/dockerfiles/14.1.1.0#start-the-container)

---

## References

- [Oracle Container Registry — WebLogic](https://container-registry.oracle.com/ords/ocr/ba/middleware/weblogic)
- [Oracle WebLogic Docker Images on GitHub](https://github.com/oracle/docker-images/tree/main/OracleWebLogic)
- [WebLogic 14.1.1.0 Release Notes](https://docs.oracle.com/en/middleware/standalone/weblogic-server/14.1.1.0/index.html)
- [Oracle WebLogic Server on Docker Containers](https://www.oracle.com/a/ocom/docs/middleware/weblogic-server-on-docker-wp.pdf)