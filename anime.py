import requests
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox
import urllib.request
import io
import random

def display_image_from_url(url, name, anime):
    root = tk.Tk()
    root.title("Guess The Character")
    try:
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
    except Exception as e:
        print(f"Error fetching image: {e}")
        return
    try:
        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    label = tk.Label(root, image=photo)
    label.pack()
    name_label = tk.Label(root, text="Name:")
    name_label.pack()
    name_box = tk.Entry(root)
    name_box.pack()
    def guessInline():
        if guess(name_box.get(), name):
            print(anime)
            root.destroy()
            root.quit()
    but = tk.Button(root, text="Guess", command=guessInline)
    but.pack()
    root.mainloop()

def guess(user_guess, name):
    print(repr(user_guess), repr(name), user_guess == name)
    return user_guess.upper().strip() == name.upper().strip()

def getRandomId():
    response = requests.get('https://api.jikan.moe/v4/random/characters?nsfw=true', timeout=2.5)
    if response:
        response = response.json()
        id = response["data"]["mal_id"]
        r2 = requests.get(f'https://api.jikan.moe/v4/characters/{id}/pictures?nsfw=true', timeout=2.5)
        if r2.status_code != 200:
            return None
        r2 = r2.json()["data"]
        if len(r2) <= 0:
            return None
        url = random.choice(r2)
        if "jpg" in url:
            url = url["jpg"]["image_url"]
        else:
            url = url["webp"]["image_url"]
        r3 = requests.get(f'https://api.jikan.moe/v4/characters/{id}/full', timeout=2.5)
        if r3.status_code != 200:
            return None
        r3 = r3.json()["data"]["anime"]
        if len(r3) <= 0:
            return None
        anime = r3[0]["anime"]["title"]
        return (response["data"]["name"], url, anime)
    return None

def main() -> None:
    while True:
        tup = getRandomId()
        if tup:
            name, url, anime = tup
            display_image_from_url(url, name, anime)

if __name__ == '__main__':
    main()