[← Back to all guides](../../../README.md)

# 02 — WLST Basics: Connect and Save Credentials

Connect to the SOA Quick Start 12c Integrated Server with WLST and save the credentials, so later scripts can connect without a password.

---

## Prerequisites

- [01 — Getting Started](../01-getting-started/) completed
- Container `soa-qs-12c` running, created with the guides mount from [01 — Step 6](../01-getting-started/#step-6--run-the-container)
- The Integrated Server **started**

> 💡 **No guides mount?** Mounts can't be added to an existing container. Either recreate it with [01 — Step 6](../01-getting-started/#step-6--run-the-container), using the same `MNT_LOC` so your domain is kept, or copy the scripts to the same path, from the `02-wlst-basics` folder:
> ```bash
> docker exec soa-qs-12c mkdir -p /u01/oracle/guides/02-wlst-basics
> docker cp scripts soa-qs-12c:/u01/oracle/guides/02-wlst-basics/
> ```

---

## Step 1 — Start WLST

```bash
docker exec -it soa-qs-12c bash
$ORACLE_HOME/oracle_common/common/bin/wlst.sh
```

---

## Step 2 — Connect

```python
connect('weblogic', '<WeblogicPassword>', 't3://localhost:7101')
```

---

## Step 3 — Save Credentials

```python
storeUserConfig('/u01/oracle/.wlst/user.config', '/u01/oracle/.wlst/user.key')
disconnect()
exit()
```

> ⚠️ Anyone who can read both files can connect as `weblogic`. In production, restrict access to both files and store a least-privileged user instead of `weblogic`.

---

## Step 4 — Connect with Saved Credentials

Run the script:

```bash
$ORACLE_HOME/oracle_common/common/bin/wlst.sh /u01/oracle/guides/02-wlst-basics/scripts/connect.py
```

The output should include:

```
Current state of "DefaultServer" : RUNNING
```

---

## References

- [WLST Command Reference for WebLogic Server 12.2.1.4](https://docs.oracle.com/en/middleware/fusion-middleware/weblogic-server/12.2.1.4/wlstc/reference.html#GUID-282E885A-57C3-45FB-9A7C-87515963B423)
