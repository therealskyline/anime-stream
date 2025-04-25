import os
import json
import logging
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, session

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "anime-zone-secret-key")

# Function to convert Google Drive URL to direct download URL
def convert_gdrive_url(url, for_download=False):
    # Extracting file ID from Google Drive URL
    match = re.search(r'\/d\/(.+?)\/view', url)
    if match:
        file_id = match.group(1)
        if for_download:
            # Lien direct pour télécharger depuis Google Drive
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        else:
            # Lien pour prévisualiser dans le navigateur
            return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

# Load anime data from JSON file
def load_anime_data():
    try:
        with open('static/data/anime.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Convert Google Drive URLs to direct download links
            for anime in data["anime"]:
                for season in anime["seasons"]:
                    for episode in season["episodes"]:
                        if "drive.google.com" in episode["video_url"]:
                            episode["video_url"] = convert_gdrive_url(episode["video_url"])
            
            return data
    except FileNotFoundError:
        # Create default data if file doesn't exist
        default_data = {
            "anime": [
                {
                    "id": 1,
                    "title": "Attack on Titan",
                    "description": "In a world where humanity lives within cities surrounded by enormous walls due to the Titans, giant humanoid beings who devour humans seemingly without reason.",
                    "image": "/static/images/anime/attack-on-titan.jpg",
                    "genres": ["action", "drama", "fantasy"],
                    "rating": 9.0,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "To You, 2000 Years Later",
                                    "description": "After 100 years of peace, humanity is suddenly reminded of the terror of being at the Titans' mercy.",
                                    "video_url": "https://drive.google.com/file/d/1MXN72LKpkLUEr7jM8tOloBgIjxNyoxdj/view?usp=drive_link"
                                },
                                {
                                    "episode_number": 2,
                                    "title": "That Day",
                                    "description": "After the Titans break through the wall, Eren vows that he will kill every Titan on earth.",
                                    "video_url": "https://drive.google.com/file/d/1MXN72LKpkLUEr7jM8tOloBgIjxNyoxdj/view?usp=drive_link"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "Demon Slayer",
                    "description": "A youth begins a quest to fight demons and save his sister after his family is slaughtered and his sister is turned into a demon.",
                    "image": "/static/images/anime/demon-slayer.jpg",
                    "genres": ["action", "fantasy", "supernatural"],
                    "rating": 8.9,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Cruelty",
                                    "description": "Tanjiro ventures out to sell charcoal but ends up staying the night at someone else's house due to rumors about a demon nearby.",
                                    "video_url": "https://example.com/video3.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 3,
                    "title": "My Hero Academia",
                    "description": "In a world where people with superpowers known as 'Quirks' are the norm, a boy without powers dreams of becoming a superhero.",
                    "image": "/static/images/anime/my-hero-academia.jpg",
                    "genres": ["action", "comedy", "superhero"],
                    "rating": 8.7,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Izuku Midoriya: Origin",
                                    "description": "Izuku Midoriya desperately wants to be a hero, but he is one of the few in his generation born without a Quirk.",
                                    "video_url": "https://example.com/video4.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 4,
                    "title": "One Punch Man",
                    "description": "The story of Saitama, a hero who can defeat any opponent with a single punch but seeks a worthy opponent after growing bored by a lack of challenge.",
                    "image": "/static/images/anime/one-punch-man.jpg",
                    "genres": ["action", "comedy", "superhero"],
                    "rating": 8.8,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "The Strongest Man",
                                    "description": "Saitama is a guy who's a hero for fun. After saving a child from certain death, he decided to become a hero and trained hard for three years.",
                                    "video_url": "https://example.com/video5.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "Death Note",
                    "description": "A high school student discovers a supernatural notebook that allows him to kill anyone by writing the victim's name while picturing their face.",
                    "image": "/static/images/anime/death-note.jpg",
                    "genres": ["mystery", "thriller", "supernatural"],
                    "rating": 9.0,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Rebirth",
                                    "description": "Light Yagami discovers a mysterious notebook that allows him to kill anyone whose name he writes in it.",
                                    "video_url": "https://example.com/video6.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 6,
                    "title": "Fullmetal Alchemist: Brotherhood",
                    "description": "Two brothers search for a Philosopher's Stone after an attempt to revive their deceased mother goes wrong and leaves them in damaged physical forms.",
                    "image": "/static/images/anime/fullmetal-alchemist.jpg",
                    "genres": ["action", "adventure", "fantasy"],
                    "rating": 9.1,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Fullmetal Alchemist",
                                    "description": "The Elric brothers adjust to military life and pursue the Philosopher's Stone in order to regain what they've lost.",
                                    "video_url": "https://example.com/video7.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 7,
                    "title": "Tokyo Ghoul",
                    "description": "A college student is attacked by a ghoul, a being that feeds on human flesh, and he becomes a half-ghoul himself.",
                    "image": "/static/images/anime/tokyo-ghoul.jpg",
                    "genres": ["horror", "supernatural", "thriller"],
                    "rating": 8.5,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Tragedy",
                                    "description": "Ken Kaneki's date turns into a nightmare when she reveals herself as a ghoul.",
                                    "video_url": "https://example.com/video8.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 8,
                    "title": "Naruto",
                    "description": "A young ninja with a sealed demon within him aspires to become the leader of his village and gain recognition from his peers.",
                    "image": "/static/images/anime/naruto.jpg",
                    "genres": ["action", "adventure", "fantasy"],
                    "rating": 8.3,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Enter: Naruto Uzumaki!",
                                    "description": "Naruto's prank puts him in trouble as he fails to graduate from the Ninja Academy for the third time.",
                                    "video_url": "https://example.com/video9.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 9,
                    "title": "Steins;Gate",
                    "description": "A group of friends create a device that can send messages to the past, but their discovery leads to unimaginable consequences.",
                    "image": "/static/images/anime/steins-gate.jpg",
                    "genres": ["sci-fi", "thriller", "drama"],
                    "rating": 9.2,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Prologue of the Beginning and End",
                                    "description": "Rintaro Okabe finds the dead body of Kurisu Makise and sends a message about it to his friend, causing him to experience strange events.",
                                    "video_url": "https://example.com/video10.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 10,
                    "title": "Hunter x Hunter",
                    "description": "A young boy sets out to become a Hunter, an elite member of society, to find his missing father, who is also a legendary Hunter.",
                    "image": "/static/images/anime/hunter-x-hunter.jpg",
                    "genres": ["action", "adventure", "fantasy"],
                    "rating": 9.1,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Departure × And × Friends",
                                    "description": "Gon Freecss wants to become a Hunter like his father, so he leaves Whale Island to take the Hunter Exam.",
                                    "video_url": "https://example.com/video11.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 11,
                    "title": "Jujutsu Kaisen",
                    "description": "A high school student swallows a cursed item and becomes cursed himself. He enters a school for exorcists to protect others from curses.",
                    "image": "https://images.unsplash.com/photo-1625189659340-887baac3ea32",
                    "genres": ["action", "supernatural", "horror"],
                    "rating": 8.7,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Ryomen Sukuna",
                                    "description": "Yuji Itadori, a high school student with extraordinary physical abilities, swallows a cursed item to protect his friends.",
                                    "video_url": "https://example.com/video12.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 12,
                    "title": "Cowboy Bebop",
                    "description": "A ragtag group of bounty hunters chase down criminals in the vastness of space in the year 2071.",
                    "image": "https://images.unsplash.com/photo-1519638399535-1b036603ac77",
                    "genres": ["sci-fi", "neo-noir", "space western"],
                    "rating": 8.9,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Asteroid Blues",
                                    "description": "The crew of the Bebop chase a criminal couple through the asteroid belt.",
                                    "video_url": "https://example.com/video13.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 13,
                    "title": "Your Lie in April",
                    "description": "A piano prodigy who lost his ability to play after suffering a traumatic event meets a violinist who helps him return to music.",
                    "image": "https://images.unsplash.com/photo-1571757767119-68b8dbed8c97",
                    "genres": ["drama", "romance", "music"],
                    "rating": 8.8,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Monotone/Colorful",
                                    "description": "Kousei Arima, a former piano prodigy who can no longer hear the notes when he plays, meets a free-spirited violinist who changes his life.",
                                    "video_url": "https://example.com/video14.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 14,
                    "title": "The Promised Neverland",
                    "description": "Orphans at Grace Field House discover the dark truth about their existence and plot an escape.",
                    "image": "https://images.unsplash.com/photo-1602416222941-a72a356dab04",
                    "genres": ["mystery", "horror", "thriller"],
                    "rating": 8.7,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "121045",
                                    "description": "Emma, Norman, and Ray enjoy their daily life at Grace Field House, unaware of the dark truth behind their existence.",
                                    "video_url": "https://example.com/video15.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 15,
                    "title": "Mob Psycho 100",
                    "description": "A psychic middle school boy tries to live a normal life and keep his growing powers under control, even as he is exploited by others.",
                    "image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f",
                    "genres": ["action", "comedy", "supernatural"],
                    "rating": 8.8,
                    "featured": True,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Self-Proclaimed Psychic: Reigen Arataka ~And Mob~",
                                    "description": "Middle school student Mob works as an assistant to a con artist who exploits Mob's psychic abilities.",
                                    "video_url": "https://example.com/video16.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 16,
                    "title": "Re:Zero",
                    "description": "After being suddenly transported to another world, a young man discovers he has the ability to rewind time by dying.",
                    "image": "https://images.unsplash.com/photo-1613376023733-0a73315d9b06",
                    "genres": ["fantasy", "drama", "thriller"],
                    "rating": 8.7,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "The End of the Beginning and the Beginning of the End",
                                    "description": "Subaru Natsuki is suddenly summoned to another world on his way home from the convenience store.",
                                    "video_url": "https://example.com/video17.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 17,
                    "title": "Vinland Saga",
                    "description": "A young Viking seeks revenge for his father's death while questioning the meaning of war and the true definition of a warrior.",
                    "image": "https://images.unsplash.com/photo-1601850494422-3cf14624b0b3",
                    "genres": ["action", "adventure", "historical"],
                    "rating": 8.8,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Somewhere Not Here",
                                    "description": "Thorfinn grows up hearing tales of old sailors about the legendary land called Vinland.",
                                    "video_url": "https://example.com/video18.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 18,
                    "title": "Made in Abyss",
                    "description": "An orphaned girl descends into a mysterious and dangerous abyss in search of her mother.",
                    "image": "https://images.unsplash.com/photo-1625189659340-887baac3ea32",
                    "genres": ["adventure", "fantasy", "sci-fi"],
                    "rating": 8.8,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "The City of the Great Pit",
                                    "description": "Riko, a young orphan girl living in the town of Orth, dreams of becoming a legendary Cave Raider like her mother.",
                                    "video_url": "https://example.com/video19.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 19,
                    "title": "Parasyte: The Maxim",
                    "description": "Alien parasites invade Earth and take over human hosts. A high school student fights to protect humanity when a parasite takes over his right hand.",
                    "image": "https://images.unsplash.com/photo-1519638399535-1b036603ac77",
                    "genres": ["horror", "sci-fi", "psychological"],
                    "rating": 8.5,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Metamorphosis",
                                    "description": "Parasitic aliens fall to Earth and take over human hosts by entering through their ears or noses.",
                                    "video_url": "https://example.com/video20.mp4"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 20,
                    "title": "Erased",
                    "description": "A man with the ability to travel back in time uses his power to solve a murder case from his childhood.",
                    "image": "https://images.unsplash.com/photo-1571757767119-68b8dbed8c97",
                    "genres": ["mystery", "thriller", "supernatural"],
                    "rating": 8.6,
                    "featured": False,
                    "seasons": [
                        {
                            "season_number": 1,
                            "episodes": [
                                {
                                    "episode_number": 1,
                                    "title": "Flashing Before My Eyes",
                                    "description": "Satoru Fujinuma has an ability he calls 'Revival,' which sends him back in time to prevent deaths.",
                                    "video_url": "https://example.com/video21.mp4"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        with open('static/data/anime.json', 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data

# Routes
@app.route('/')
def index():
    data = load_anime_data()
    featured_anime = [anime for anime in data['anime'] if anime.get('featured', False)][:15]
    # Get a unique list of all genres for filter buttons
    all_genres = set()
    for anime in data['anime']:
        all_genres.update(anime.get('genres', []))
    
    return render_template('index.html', 
                          anime_list=featured_anime, 
                          genres=sorted(all_genres))

@app.route('/search')
def search():
    query = request.args.get('query', '')
    genre = request.args.get('genre', '')
    
    data = load_anime_data()
    anime_list = data['anime']
    
    # Filter by search query if provided
    if query:
        anime_list = [anime for anime in anime_list if query.lower() in anime['title'].lower()]
    
    # Filter by genre if provided
    if genre:
        anime_list = [anime for anime in anime_list if genre.lower() in [g.lower() for g in anime.get('genres', [])]]
    
    # Get all genres for filter buttons
    all_genres = set()
    for anime in data['anime']:
        all_genres.update(anime.get('genres', []))
    
    return render_template('search.html', 
                          anime_list=anime_list, 
                          query=query,
                          selected_genre=genre,
                          genres=sorted(all_genres))

@app.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    data = load_anime_data()
    anime = next((a for a in data['anime'] if a['id'] == anime_id), None)
    
    if not anime:
        return render_template('404.html'), 404
    
    return render_template('anime.html', anime=anime)

@app.route('/player/<int:anime_id>/<int:season>/<int:episode>')
def player(anime_id, season, episode):
    data = load_anime_data()
    anime = next((a for a in data['anime'] if a['id'] == anime_id), None)
    
    if not anime:
        return render_template('404.html'), 404
    
    selected_season = next((s for s in anime['seasons'] if s['season_number'] == season), None)
    
    if not selected_season:
        return render_template('404.html'), 404
    
    selected_episode = next((e for e in selected_season['episodes'] if e['episode_number'] == episode), None)
    
    if not selected_episode:
        return render_template('404.html'), 404
    
    # Conserver l'URL originale
    original_url = selected_episode["video_url"]
    
    # URL pour le téléchargement - utilisation directe de l'URL spécifiée
    download_url = "https://drive.google.com/uc?export=download&id=1MXN72LKpkLUEr7jM8tOloBgIjxNyoxdj"
    
    # URL pour la lecture (iframe)
    if "drive.google.com" in original_url:
        selected_episode["video_url"] = convert_gdrive_url(original_url)
    
    return render_template('player.html', 
                          anime=anime, 
                          season=selected_season, 
                          episode=selected_episode,
                          download_url=download_url)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/categories')
def categories():
    data = load_anime_data()
    
    # Get all unique genres
    all_genres = set()
    for anime in data['anime']:
        all_genres.update(anime['genres'])
    
    # Create a dictionary of genres and their anime
    genres_dict = {}
    for genre in sorted(all_genres):
        genres_dict[genre] = [anime for anime in data['anime'] if genre in anime['genres']]
    
    return render_template('categories.html', genres_dict=genres_dict, all_anime=data['anime'], genres=sorted(all_genres))

# Routes administratives supprimées pour permettre à l'utilisateur de les ajouter manuellement

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
