[← Back to all guides](../../../README.md)

# 03 — Users and Groups with WLST

Create the group `HelloUsers` and the user `hello_user` with WLST. Later guides use this user to call protected endpoints.

---

## Prerequisites

- [02 — WLST Basics](../02-wlst-basics/) completed (saved credentials)
- Container `soa-qs-12c` running, with the Integrated Server **started**

> 💡 **No guides mount?** Copy the scripts to the same path, from the `03-users-and-groups` folder:
> ```bash
> docker exec soa-qs-12c mkdir -p /u01/oracle/guides/03-users-and-groups
> docker cp scripts soa-qs-12c:/u01/oracle/guides/03-users-and-groups/
> ```

---

## Step 1 — Create the User and Group

```bash
docker exec -it soa-qs-12c bash
$ORACLE_HOME/oracle_common/common/bin/wlst.sh /u01/oracle/guides/03-users-and-groups/scripts/create_user.py
```

Enter and confirm the password for `hello_user` when prompted. It must have at least 8 characters, including a number or special character. Remember it; later guides need it.

> 💡 **Options:** `.../create_user.py [-u <user>] [-g <group>] [-p <password>]`. Later guides assume the defaults `hello_user` / `HelloUsers`. A password passed with `-p` is kept in your shell history.

The script is safe to rerun. An existing user keeps its password.

---

## Step 2 — Verify

The output should include:

```
Created group HelloUsers
Created user hello_user
hello_user is a member of HelloUsers
```

---

## References

- [WLST Command Reference for WebLogic Server 12.2.1.4](https://docs.oracle.com/en/middleware/fusion-middleware/weblogic-server/12.2.1.4/wlstc/reference.html#GUID-282E885A-57C3-45FB-9A7C-87515963B423)
- [Securing Resources Using Roles and Policies for WebLogic Server 12.2.1.4](https://docs.oracle.com/en/middleware/fusion-middleware/weblogic-server/12.2.1.4/roles/index.html)
