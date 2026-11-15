
# Ubuntu VM Setup — Reference Guide

Essential install and disk expansion commands for new Ubuntu VMs. Tested on Hyper-V, Ubuntu (jammy).

---

## 1. System update (run first, always)

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 2. curl

```bash
sudo apt install -y curl
```

---

## 3. uv (Python package/version manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
echo 'source $HOME/.local/bin/env' >> ~/.bashrc
```

Install a Python version via uv (optional, recommended):

```bash
uv python install 3.12
```

---

## 4. Python (system-level)

```bash
sudo apt install -y python3 python3-pip python3-venv
```

---

## 5. VS Code (via curl / official Microsoft repo, no snap)

```bash
sudo apt install -y wget gpg apt-transport-https
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
rm packages.microsoft.gpg

sudo apt update
sudo apt install -y code
```

---

## 6. Node.js

**Option A — NodeSource (system-wide, single version, simplest)**

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

**Option B — nvm (multiple Node versions)**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc

nvm install --lts
nvm use --lts
```
*Check the [nvm releases page](https://github.com/nvm-sh/nvm/releases) for the current version tag before running.*

---

## 7. npm global install permissions fix

Needed if `npm install -g` fails with `EACCES` (common when Node came from apt, since `/usr` is root-owned).

```bash
npm config get prefix   # if this prints /usr, fix below

mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 8. Verify everything

```bash
curl --version
uv --version
python3 --version
code --version
node --version
npm --version
```

---

## 9. Disk / partition expansion (after resizing VHD in Hyper-V Manager)

Resizing the virtual disk in Hyper-V only grows the VHD — the partition and filesystem inside Ubuntu must be grown separately.

**Step 1 — check current state**

```bash
df -h /
lsblk
df -T /        # confirms filesystem type (ext4/xfs)
```

**Step 2 — confirm kernel sees new disk size**

```bash
sudo dmesg | grep -i sda
```

If not reflected, rescan or reboot:

```bash
echo 1 | sudo tee /sys/class/block/sda/device/rescan
```

**Step 3 — grow the partition**

```bash
sudo apt install -y cloud-guest-utils
sudo growpart /dev/sda 1        # replace 1 with correct partition number from lsblk
```

**Step 4 — grow the filesystem**

ext4:
```bash
sudo resize2fs /dev/sda1
```

xfs:
```bash
sudo xfs_growfs /
```

**Step 5 — verify**

```bash
df -h /
```

### If on LVM (check first with `sudo lvs` / `sudo vgs`)

Only run this branch if those commands return actual volume groups/logical volumes. Skip entirely on plain-partition setups (confirmed not needed on this VM).

```bash
sudo pvresize /dev/sda3                              # whichever partition is the PV
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv               # or xfs_growfs / if xfs
```

---

## Notes / gotchas

- **VS Code headless VMs:** `code` won't launch a GUI window on a headless server — use `code-server` or VS Code Remote-SSH from your local machine instead.
- **Low disk space breaks npm installs:** npm can fail or misbehave with under ~500MB free. If a global install fails right after setup, check `df -h` before debugging further.
- **OpenClaw install command:**
  ```bash
  curl -fsSL https://openclaw.ai/install.sh | bash
  ```
  If it fails, re-run the underlying npm command directly with verbose logging to see the real error (installer temp logs can vanish on retry):
  ```bash
  npm --loglevel verbose --no-fund --no-audit --min-release-age=0 install -g openclaw@latest
  ```
