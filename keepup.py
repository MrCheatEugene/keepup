import asyncio
import aiohttp

minutes = 1  # delay between checks
ip = '1.1.1.1'  # server ip

vmmanager_id = ''  # server id from vm.aeza.net
aeza_id = ''  # server id from my.aeza.net

login = ''  # login/email from my.aeza.net
password = ''  # password from my.aeza.net


async def ping(ip):
  async with aiohttp.ClientSession() as session:
    try:
      async with session.get('http://' + ip, timeout=1) as resp:
        print(resp.status)
        return True
    except aiohttp.client_exceptions.ServerDisconnectedError as e:
      print(repr(e))
      print('Server offline')
      return False
    except asyncio.exceptions.TimeoutError as e:
      print(repr(e))
      print('Server offline')
      return False


async def reboot():
  async with aiohttp.ClientSession() as session:
    headers = {'authorization': 'Bearer undefined'}
    json = {'method': 'credentials', 'email': login, 'password': password}
    async with session.post('https://core.aeza.net/api/auth?',
                            headers=headers,
                            json=json) as resp:
      json_ = await resp.json()
    api_key = json_['data']['session']
    headers = {'authorization': f'Bearer {api_key}'}
    async with session.get(
        f'https://core.aeza.net/api/services/{aeza_id}/goto?',
        headers=headers) as resp:
      json_ = await resp.json()
    keyvm = json_['data'].split('key/')[1]
    json = {'key': keyvm}
    async with session.post('https://vm.aeza.net/auth/v3/auth_by_key',
                            json=json) as resp:
      json_ = await resp.json()
    sesskey = json_['session']
    real_keyvm = json_['token']
    cookies = {'token': real_keyvm, 'ses6': sesskey}
    headers = {'x-xsrf-token': real_keyvm}
    async with session.post(
        f'https://vm.aeza.net/vm/v3/host/{vmmanager_id}/start',
        cookies=cookies,
        headers=headers) as resp:
      respjson = await resp.json()
  if 'id' in respjson:
    print('УСПЕХ! Машинка автоматически запущена!')
  else:
    print(f'Ошибка. Не удалось запустить виртуальную машину. JSON-ответ: {respjson}')


async def main():  #reboot server if ping error 5 times in a row
  error_count = 0

  while True:
    for i in range(5):
      if await ping(ip):
        error_count = 0
      else:
        error_count += 1
        if error_count == 5:
          await reboot()
          break
    await asyncio.sleep(60 * minutes)


asyncio.run(main())
