from time import sleep

from selenium import webdriver

from pytube import YouTube

options = webdriver.ChromeOptions()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#options.add_argument('--headless')


def save_links(playlist_link):
    links = []

    with webdriver.Chrome(options=options) as browser:

        browser.get(playlist_link)
        videos = browser.find_elements_by_tag_name('ytd-playlist-video-renderer')

        for video in videos:
            links.append(video.find_element_by_id('content').find_element_by_tag_name('a').get_attribute('href'))
    
    with open('links.txt', 'a+') as file:
        for link in links:
            file.write(f'{link} \n')


def get_links():
    with open('links.txt', 'r') as file:
        return file.readlines()


def get_safe_links():
    with open('safe-links.txt', 'r') as file:
        return file.readlines()

def save_descriptions(links):
    descriptions = []
    safe_links = []

    with webdriver.Chrome(options=options) as browser:
        for link in links:
            browser.get(link.split(' \n')[0])
            sleep(5)
            description = browser.find_element_by_id('description').get_attribute('textContent')

            try:
                """
                This following code requires a try-except since it will directly try to split the descriptions.
                The problem is: If the video of the playlist does not have the following "sanitizing-flags",
                it will raise an exception.
                """
                sanitize = description.split('––– ARTIST CREDIT INSTRUCTIONS –––')[1].split('• (C) Copyright Notice:')[0]
                sanitize = sanitize.strip().split('\n')

                for string in sanitize:
                    if string.startswith('► You’re free to use') or string.startswith('● You’re able to use'):
                        sanitize.remove(string)

                sanitize = '\n'.join(sanitize)

                for trash in ['(Copy Below Paragraph)', '(Start Copy/Paste Below)', '(END Copy/Paste Above)']:
                    sanitize = sanitize.replace(trash, '')
                
                print(sanitize)
                descriptions.append(sanitize)
                safe_links.append(link)
            except IndexError:
                """
                Remove the '# ' part of the next line if you want to save the description no matter what.
                If you're like me, who just wants the descriptions ( and videos with that being said ) of the
                Chill Out [No Copyright] channel let this commented.

                Note: Pay very attention to the descriptions if you're a youtuber. Sometimes, youtube add random videos
                on the playlists, and you can download some music that have copyright. For security sake, I let the following
                part commented, so the only videos it'll download, are the onlys that have no copyright.
                """
                # descriptions.append(description)
                continue


    with open('descriptions.txt', 'a+', encoding='utf8') as file:
       for description in descriptions:
          file.write(f'{description} \n\n\n')

    with open('safe-links.txt', 'a+', encoding='utf8') as file:
        for safe_link in safe_links:
            file.write(safe_link)

    for index, description in enumerate(descriptions):
        with open(f'../descriptions/{index}.txt', 'w+', encoding='utf8') as file:
            file.write(description)


def download_videos(links):
    for link in links:
        try:
            YouTube(link).streams.filter(only_audio=True).first().download('../')
        except:
            print('Failed to download video at link', link)


def download_safe_videos(safe_links):
    for index, link in enumerate(safe_links):
        while True:
            try:
                YouTube(link).streams.filter(only_audio=True).first().download(output_path='../videos/', filename=str(index))
                break
            except:
                print(f'Failed to download video {link} at index {index}. Trying again.')


#save_links('https://www.youtube.com/playlist?list=PL06diOotXAJLAAHBY7kIUm5GQwm2ZinOz')

links = get_links()

save_descriptions(links)

safe_links = get_safe_links()

#download_videos(links)
download_safe_videos(safe_links)


"""
Never forget to always look to the descriptions, videos and video titles.
Although the code is very stable, youtube is not, it might show you a music video that is copyrighted.
The best approach is to always check. See if the video titles explicitly say about non-copyrighted material.
Check if the artist' info weren't cut out, etc ...
If you're in doubt about the video, if it's copyrighted or not, don't use it.
"""
