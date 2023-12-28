# Development

Using VM instead of devcontainer to test in full HAOS

```bash
# Install UTM and QEMU
brew install --cask utm
brew install qemu

# Download and configure VM (aarch64)
python3 ./dev/configure.py

# Store the IP address of the virtual machine
VM_IP=$(osascript -e 'tell application "UTM" to get item 1 of (query ip of virtual machine named "HAOS")')

# Onboarding
echo "http://${VM_IP}:8123" | xargs open

# Install addon "Advanced SSH & Web Terminal"
echo "http://${VM_IP}:8123/hassio/addon/a0d7b954_ssh/info" | xargs open

# username: root
# sftp: true
# authorized_keys: ...
cat ~/.ssh/id_rsa.pub

# Copy addon-ha-fusion
rsync -avz \
  ~/Developer/addon-ha-fusion \
  root@${VM_IP}:/root/addons/ && \
rsync -avz \
  ~/Developer/ha-fusion/ \
  --exclude 'node_modules' \
  --exclude '.git' \
  --exclude '.env' \
  root@${VM_IP}:/root/addons/addon-ha-fusion/rootfs
```

## Important

* Use **local** and comment out **remote** in `Dockerfile`
* Comment out `image:` in `config.yaml`
