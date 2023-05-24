import asyncio
import aiohttp
from aiohttp.client_exceptions import ServerDisconnectedError
from asyncio.exceptions import TimeoutError

class Config:
    def __init__(self):
        self.minutes = 1  # delay between checks
        self.ip = '1.1.1.1'  # server ip
        self.vmmanager_id = ''  # server id from vm.aeza.net
        self.aeza_id = ''  # server id from my.aeza.net
        self.login = ''  # login/email from my.aeza.net
        self.password = ''  # password from my.aeza.net
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

config = Config()

async def ping():
    try:
        async with config.session.get(f'http://{config.ip}', timeout=1) as resp:
            print(resp.status)
            return True
    except (ServerDisconnectedError, TimeoutError) as e:
        print(repr(e))
        print('Server offline')
        return False

async def get_auth_key():
    headers = {'authorization': 'Bearer undefined'}
    json = {'method': 'credentials', 'email': config.login, 'password': config.password}
    async with config.session.post('https://core.aeza.net/api/auth?',
                                    headers=headers,
                                    json=json) as resp:
        json_ = await resp.json()
    return json_['data']['session']

async def get_vm_key(auth_key):
    headers = {'authorization': f'Bearer {auth_key}'}
    async with config.session.get(
            f'https://core.aeza.net/api/services/{config.aeza_id}/goto?',
            headers=headers) as resp:
        json_ = await resp.json()
    return json_['data'].split('key/')[1]

async def start_vm(vm_key, auth_key):
    json = {'key': vm_key}
    async with config.session.post('https://vm.aeza.net/auth/v3/auth_by_key',
                                    json=json) as resp:
        json_ = await resp.json()
    sesskey = json_['session']
    real_keyvm = json_['token']
    cookies = {'token': real_keyvm, 'ses6': sesskey}
    headers = {'x-xsrf-token': real_keyvm}
    async with config.session.post(
            f'https://vm.aeza.net/vm/v3/host/{config.vmmanager_id}/start',
            cookies=cookies,
            headers=headers) as resp:
        respjson = await resp.json()
    if 'id' in respjson:
        print('Success! The virtual machine has been automatically started.')
    else:
        print(f'Error. Failed to start the virtual machine. JSON response: {respjson}')

async def reboot():
    auth_key = await get_auth_key()
    vm_key = await get_vm_key(auth_key)
    await start_vm(vm_key, auth_key)

async def main():  #reboot server if ping error 5 times in a row
    error_count = 0

    while True:
        for i in range(5):
            if await ping():
                error_count = 0
            else:
                error_count += 1
                if error_count == 5:
                    await reboot()
                    break
        await asyncio.sleep(60 * config.minutes)

async def run():
    try:
        await main()
    finally:
        await config.close()

asyncio.run(run())
