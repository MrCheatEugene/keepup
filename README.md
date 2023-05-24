# keepup

Auto-restart for Aeza's AMS-PROMO servers. Supports authorization by API key, and by login/password.

## Setting up

1. Install Python 3.7 and the `requests` library.
2. Clone the repository.
3. Copy `keepup.py` to whatever location you want. If you have multiple VMs, just copy and paste the script, and set everything up one-by-one.
4. Open the script with your favorite editor (vim, nano, vscode, etc.).
5. On line 6, you will see the `host_id` variable. This is a VM's ID in VMManager. It starts with #, like: `*vm00000000* **#12345**`. The `12345` part is it.
6. On line 7, you will see the `aeza_id` variable. This is an Aeza's VM ID. You can find it by going to any service page, like `https://my.aeza.net/services/000000`, where `0000000` will be that ID.
7. On line 9, there is a `type_auth` variable. `"login"` means authentication via login and password, and `"direct"` means authentication by an API key, which can be obtained [here](https://my.aeza.net/settings/apikeys). Set login/password variables to the login and password for Aeza's dashboard account, or if you're using key-based authorization, set the `key` variable to a valid API key. Note: If you have 2FA enabled on your account, authentication will only be possible with an API key.
8. Save your changes and close the editor.

## Setting up as a systemd service

If you want to run the script continuously as a service on a Linux system that uses systemd, you can follow these steps:
1. Create a systemd service file, usually located in `/etc/systemd/system/`, for example `sudo nano /etc/systemd/system/keepup.service`.
2. Add the following to the file:
```
[Unit]
Description=KeepUp Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/keepup.py
Restart=always
User=yourusername
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```
Replace `/path/to/keepup.py` with the actual path to the `keepup.py` script, and `yourusername` with the name of the user that should run the script.
3. Save the file and close the editor.
4. Enable the service to start on boot using `sudo systemctl enable keepup`.
5. Start the service now using `sudo systemctl start keepup`.

## Code Quality

This script is constantly improving, and has been refactored to follow best practices for Python programming.

## License

This script is licensed by the Unlicense License. This means that anybody can use it, absolutely free, no attribution required, even in commercial setups. Because this script is now in the public domain. Again. Free to use, free to copy, free to modify. By anybody.
