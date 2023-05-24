import requests
# НАСТРОЙКИ

host_id="000000" # Номер машины в VMManager (указан в списке машин, писать без #)
aeza_id="000000" # Номер машины в панели Aeza (указан в URL, https://my.aeza.net/services/000000)

type_auth="login" # Тип входа (login - по логину и паролю, direct - API ключ напрямую)

# login
login="admin@example.org" # e-mail 
password="12345678" # пароль

#direct
key="AAAAAAAAAAAAAAAAAAAAA"

try:
	r = requests.get("http://1.1.1.1") # Тут любой удобный метод, на проверку машины. Суть в том, чтобы в случае неудачи оно выплюнуло Exception :) 
	# Лично я тут указываю IP адрес сервера, и накатываю на сервер NGINX. Самый простой метод, как по мне
except:
	if type_auth=="login":
		key = requests.post("https://core.aeza.net/api/auth?",json={"method": "credentials", "email": login, "password": password},headers={"authorization": "Bearer undefined"}).json()['data']['session']
	r=requests.get("https://core.aeza.net/api/services/346290/goto?",headers={"authorization": "Bearer "+key})
	keyvm = r.json()['data'].replace("https://vm.aeza.net/auth/key/","")
	r = requests.post("https://vm.aeza.net/auth/v3/auth_by_key",headers={"cookie":"_ym_d=1669657718; _ym_uid=1669657718468356443; ref=344585; _ym_isad=1; _ym_visorc=w; token="+key+"; ses6="+keyvm},json={"key":keyvm})
	sess = r.json()
	sesskey = sess['session']
	real_keyvm = sess['token']
	resp = requests.post("https://vm.aeza.net/vm/v3/host/"+host_id+"/start",headers={"cookie":"_ym_d=1669657718; _ym_uid=1669657718468356443; ref=344585; _ym_isad=1; _ym_visorc=w; token="+real_keyvm+"; ses6="+sesskey,"x-xsrf-token":real_keyvm})
	respjson = resp.json()
	if('id' in respjson):
		print("УСПЕХ! Машинка автоматически запущена!")
	else:
		print("Ошибка. Не удалось запустить виртуальную машину. JSON-ответ:")
		print(respjson)
