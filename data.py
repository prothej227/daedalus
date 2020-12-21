def movies():
    movies = [
        {
            'id': 1,
            'title': 'Onward',
            'body': 'Teenage elf brothers Ian and Barley embark on a magical quest to spend one more day with their late father. Like any good adventure, their journey is filled with cryptic maps, impossible obstacles and unimaginable discoveries. But when dear Mom finds out her sons are missing, she teams up with the legendary manticore to bring her beloved boys back home',   
            'year': '2020',
            'link': '/static/media/videos/movies/FlaskTV - Onward.mp4',
            'poster': '/static/img/posters/onward.jpg',
            'genre': 'Animation/Family/Comedy'
        },
        {
            'id': 2,
            'title': 'Arrival',
            'body': 'Louise Banks, a linguistics expert, along with her team, must interpret the language of aliens who\'ve come to earth in a mysterious spaceship.',   
            'link': '/static/media/videos/movies/FlaskTV - Arrival.mp4',
            'poster': '/static/img/posters/arrival.jpg',
            'year': '2016',
            'genre': 'Sci-Fi'
        },

    ]
    return movies

def series():
    series = [
        {
            'id': 1,
            'title': 'Money Heist (S01)',
            'body': 'An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history - stealing 2.4 billion euros from the Royal Mint of Spain.',   
            'year': '2017',
            'ep': '13',
            'locator': '/static/media/videos/series/money_heist/',
            'poster': '/static/img/posters/money_heist.jpg',
            'genre': 'Crime/Drama'
        },
        
    ]
    return series
