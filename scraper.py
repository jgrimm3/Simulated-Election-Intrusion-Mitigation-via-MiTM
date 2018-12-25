from bs4 import BeautifulSoup
import requests
import time
import array

page_link ='http://users.wpi.edu/~rdwirkala/'

while True:
	# fetch the content from url
	page_response = requests.get(page_link, timeout=5)

	# parse html
	page_content = BeautifulSoup(page_response.content, "html.parser")

	page_content = str(page_content)
	out = (page_content.split('<br/>'))

	i = 0
	j = 0

	# Create votes array, first index will be votes for yeezys, second will be for crocs
	votes = array.array('i', [0, 0])

	while i < len(out):
		if("Yeezy" in out[i] or "Crocs" in out[i]):
			print(out[i])
			votes[j] = int(''.join(filter(str.isdigit, out[i])))
			j += 1
		i += 1
	time.sleep(2)

# Optional sanity check print out
# print(votes[0], votes[1])
