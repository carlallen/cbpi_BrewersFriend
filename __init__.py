from modules import cbpi
import requests

bf_uri = "https://log.brewersfriend.com/stream/"

def bf_api_key():
  api_key = cbpi.get_config_parameter('brewersfriend_api_key', None)
  if api_key is None:
    cbpi.add_config_parameter("brewersfriend_api_key", "", "text", "BrewersFriend API Key")
    return ""
  else:
    return api_key


@cbpi.backgroundtask(key="brewersfriend_task", interval=600)
def brewersfriend_background_task(api):
  api_key = bf_api_key()
  if api_key == "":
    return

  for i, fermenter in cbpi.cache.get("fermenter").iteritems():
    if fermenter.state is not False:
      try:
        name = fermenter.name
        temp = fermenter.instance.get_temp()
        unit = cbpi.get_config_parameter("unit", "C")
        data = {"name": name, "temp": temp, "temp_unit": unit}
        response = requests.post(bf_uri + api_key, json=data)
      except:
        pass
