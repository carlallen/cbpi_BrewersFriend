from modules import cbpi
import requests

bf_uri = "https://log.brewersfriend.com/stream/"

def bf_api_key():
  api_key = cbpi.get_config_parameter('brewersfriend_api_key', None)
  if api_key is None:
    try:
      cbpi.add_config_parameter("brewersfriend_api_key", "", "text", "BrewersFriend API Key")
      return ""
    except:
      cbpi.notify("Brewer's Friend Error", "Unable to update brewersfriend_api_key parameter within database. Try updating CraftBeerPi and reboot.", type="danger", timeout=None)
  else:
    return api_key


@cbpi.backgroundtask(key="brewersfriend_task", interval=600)
def brewersfriend_background_task(api):
  api_key = bf_api_key()
  if api_key == "":
    cbpi.notify("Brewer's Friend Error", "API key not set. Update brewersfriend_api_key parameter within System > Parameters.", type="danger", timeout=None)
    return

  for i, fermenter in cbpi.cache.get("fermenter").iteritems():
    if fermenter.state is not False:
      try:
        name = fermenter.name
        temp = fermenter.instance.get_temp()
        unit = cbpi.get_config_parameter("unit", "C")
        data = {"name": name, "temp": temp, "temp_unit": unit}
        response = requests.post(bf_uri + api_key, json=data)
        if response.status_code != 200:
          cbpi.notify("Brewer's Friend Error", "Received unsuccessful response from Brewer's Friend on submission. Ensure your API key is correct.", type="danger", timeout=None)
      except:
        cbpi.notify("Brewer's Friend Error", "Unable to send message.", type="danger", timeout=None)
        pass
