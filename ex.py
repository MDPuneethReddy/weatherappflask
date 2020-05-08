import requests
city=input()
address="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=45bddb0e44301c13b2e98836fd385505"
json_data = requests.get(address).json()
format_add = json_data['base']
print(json_data)
