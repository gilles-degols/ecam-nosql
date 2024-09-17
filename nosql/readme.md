
## Installation issue on Windows / WSL (Ubuntu)

When following https://docs.docker.com/engine/install/ubuntu/ you might encounter at some point the following issue:

```
/sbin/ldconfig.real: Can't link /usr/lib/wsl/lib/libnvoptix_loader.so.1 to libnvoptix.so.1
/sbin/ldconfig.real: /usr/lib/wsl/lib/libcuda.so.1 is not a symbolic link
```

To solve it: https://superuser.com/questions/1707681/wsl-libcuda-is-not-a-symbolic-link

## Cannot connect to docker

Executing any docker command like "docker ps" leads to:

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

To (maybe) solve it:

```
sudo service docker start
```