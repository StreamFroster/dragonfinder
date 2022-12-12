import requests

# THIS DOES NOT WORK YET, BUT I WANT TO LEARN HOW TO DO IT SO I'LL LEAVE IT HERE

# Copilot stimulus:
# This program uses the built in python requests model to programmatically download images from e926 tagged with 'dragon'

def main():
    # get the html from e926
    # make the request with a Dragonfinder user agent
    response = requests.get('https://e926.net/posts?tags=dragon', headers={'User-Agent': 'DragonFinder/1.0 StreamFroster'})
    # get the json from the response
    json = response.json()
    # get the images from the json
    images = json['posts']
    # print the first image's url
    print(images[0]['file_url'])
    # download the first image
    r = requests.get(images[0]['file_url'])
    # open the first image in the current directory
    with open('dragon.jpg', 'wb') as f:
        # write the image to the file
        f.write(r.content)
    # make sure the request was successful
    if response.status_code != 200:
        print('Request failed with status code: {}'.format(response.status_code))
        return
    # get the json from the response
    data = response.json()
    # get the image urls from the json
    image_urls = [image['file_url'] for image in data]
    # loop through the image urls
    for url in image_urls:
        # download the image
        response = requests.get(url)
        # make sure the request was successful
        if response.status_code != 200:
            print('Request failed with status code: {}'.format(response.status_code))
            return
        # write the image to the file system
        with open('dragon_images/{}'.format(url.split('/')[-1]), 'wb') as image_file:
            image_file.write(response.content)


