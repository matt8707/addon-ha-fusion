import os
import json
import urllib.request
import subprocess
import time
from urllib.parse import urlparse


def progress(block_num, block_size, total_size):
    percent = block_num * block_size / total_size * 100
    print(
        f"Downloaded {block_num * block_size} bytes ({percent:.2f}%) of {total_size} bytes",
        end="\r",
    )


def download_file(download_url, filename):
    print(f"Downloading {download_url}")
    urllib.request.urlretrieve(download_url, filename, reporthook=progress)


def extract_file(xz_file):
    print(f"Extracting {xz_file}...")
    extract_command = f"xz -d {xz_file}"
    subprocess.run(extract_command, shell=True, check=True)


def resize_qcow2_file(qcow2_file):
    print(f"Resizing {qcow2_file}...")
    resize_command = f"qemu-img resize {qcow2_file} +32G"
    subprocess.run(resize_command, shell=True, check=True)


def create_vm_with_applescript(qcow2_file):
    applescript_command = f"""
    tell application "UTM"
        set iso to POSIX file "{qcow2_file}"
    make new virtual machine with properties {{backend:qemu, configuration:{{name:"HAOS", architecture:"aarch64", hypervisor:true, machine:"virt", uefi:true, cpu cores:0, memory:4096, network interfaces:{{hardware:"virtio-net-pci", mode:bridged, host interface:"en0"}}, drives:{{source:iso}}}}}}
    end tell
    """
    subprocess.run(["osascript", "-e", applescript_command], check=True, text=True)


def start_vm():
    start_vm_command = 'tell application "UTM" to start virtual machine named "HAOS"'
    subprocess.run(["osascript", "-e", start_vm_command], check=True, text=True)
    print("VM started successfully!")


def main():
    url = "https://api.github.com/repos/home-assistant/operating-system/releases/latest"
    with urllib.request.urlopen(url) as response:
        assets = json.loads(response.read()).get("assets", [])
        for asset in assets:
            if "aarch64" in asset["name"] and "qcow2" in asset["name"]:
                download_url = asset["browser_download_url"]
                parsed_url = urlparse(download_url)
                filename = os.path.basename(parsed_url.path)
                break

    downloaded_xz_file = os.path.expanduser(f"~/Downloads/{filename}")
    extracted_qcow2_file = os.path.expanduser(f"~/Downloads/{filename[:-3]}")

    try:
        download_file(download_url, downloaded_xz_file)
        extract_file(downloaded_xz_file)
        resize_qcow2_file(extracted_qcow2_file)
        create_vm_with_applescript(extracted_qcow2_file)
        start_vm()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
