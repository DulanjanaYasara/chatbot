import requests

# Make a get request to get the latest position of the international space station from the opennotify api.
response = requests.get("http://api.open-notify.org/iss-now.json")

# Print the status code of the response.
print(response.status_code)

# error insufficient amount of arguments (2 arguments are needed)
response = requests.get("http://api.open-notify.org/iss-pass.json")
print(response.status_code)

# hence the correct
response = requests.get("http://api.open-notify.org/iss-pass.json?lat=5&lon=80")
print(response.status_code)
# or
parameters = {"lat": 5, "lon": 80}
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
# print(response.content)


# response to string
print(response.content.decode("utf-8"))

# Get the response as a Python object
data = response.json()
print(data)

# Headers is a dictionary
print(response.headers)

# Get the content-type from the dictionary.
print(response.headers["content-type"])  # This is the most important parameter check whether this is JSON
