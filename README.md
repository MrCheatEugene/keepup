# keepup
Auto-restart for Aeza's AMS-PROMO servers. Supports authorization by API key, and by login/password

# Setting up

0. Install Python 3.7 and requests library
1. Clone the repo
2. Copy keepup.py to whatever location you want (if you have multiple VMs, just copy&paste the script, and set everything up, one-by-one)
3. Open it with your favourite editor(vim, nano, vscode, idk)
4. On line 4, you will see "host_id" variable. That is a VM's ID in VMManager. It starts with #, like: *vm00000000* **#12345**. The 12345 part is it. 
5. On line 5, you will see "aeza_id" variable. That's an Aeza's VM ID. You can find it by going onto any service page, like https://my.aeza.net/services/000000, where **0000000** will be that ID.
6. On line 7, there is a "type_auth" variable. "login" meand log/pass authentification, and "direct" means authentification by a real api key, that can be obtained [here](https://my.aeza.net/settings/apikeys). Set login/password variables to login and password for Aeza's dashboard account, or if you're using key-based authorization, set the "key" variable to a valid API key.
7. Close the editor, add a script to cron( `crontab -e` ), like this: `*/5 * * * * /usr/bin/python3 /path/to/keepup.py >/dev/null 2>&1
`.
8. Close the crontab's editor, save your changes, and now, we're done.

# Credits

Thanks to [@ArifJanMC](https://github.com/ArifJanMC), [rekayno](https://github.com/rekayno) for re-writing the whole thing, and removing low-quality code from me :)

# License

This script is licensed by Unlicense License. This means, that anybody can use it, absolutely free, no attribution required, even in commercial setups. **Because this script is now in a public domain.** Again. **Free to use, free to copy, free to modify**. By **anybody**.
