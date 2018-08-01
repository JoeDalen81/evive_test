import json
import urllib2
from datetime import datetime
import time
import sys

def query(total_pages, main_url, name, date, action, message):
    movie_dict = {}
    for i in range(1, total_pages):

        try:
            movies = json.loads(urllib2.urlopen(main_url + str(i)).read())
        except urllib2.HTTPError:
            time.sleep(10)
            movies = json.loads(urllib2.urlopen(main_url + str(i)).read())

        for content in movies['results']:
            title = content[name]
            id = content['id']

            try:
                credit_url = 'http://api.themoviedb.org/3/{a}/{b}/credits?api_key=606aaffd7ca10f0b80804a1f0674e4e1'.format(a=action,b=str(id))
            except urllib2.HTTPError:
                time.sleep(10)
                credit_url = 'http://api.themoviedb.org/3/{a}/{b}/credits?api_key=606aaffd7ca10f0b80804a1f0674e4e1'.format(a=action,b=str(id))

            try:
                credits = json.loads(urllib2.urlopen(credit_url).read())
            except urllib2.HTTPError:
                time.sleep(10)
                credits = json.loads(urllib2.urlopen(credit_url).read())

            cast = credits['cast']
            cast_list = []
            for character in cast:
                cast_list.append(character['name'])
            movie_dict[title] = {'release_date' : content[date], 'cast': cast_list}

        sys.stdout.write("    {m} {a} out of {b} pages\r".format(m=message,a=str(i),b=str(total_pages)))
        sys.stdout.flush()
    return movie_dict

def compare(result_movies, result_tv):
    movies = json.loads(result_movies)
    tv = json.loads(result_tv)
    compare_dict = {}

    for k in movies:
        movie_list = []
        tv_list = []
        a = movies[k]['cast']
        for key in tv:
            b = tv[key]['cast']

            result = set(a).intersection(b)
            if len(result) > 0: 

                for val in result:
                    movie_name = k + ": Release Date - " + movies[k]['release_date']
                    tv_name = key + ": Release Date - " + tv[key]['release_date']
                    
                    if movie_name not in movie_list:
                        movie_list.append(movie_name)
                        
                    if tv_name not in tv_list:
                        tv_list.append(tv_name)
                        
                    compare_dict[val] = {'movies': movie_list, "tv": tv_list}
    return compare_dict

def movies():
    try:
        movies = json.loads(urllib2.urlopen('http://api.themoviedb.org/3/discover/movie?primary_release_date.gte=2017-12-01&primary_release_date.lte=2017-12-31&api_key=606aaffd7ca10f0b80804a1f0674e4e1').read())
    except urllib2.HTTPError:
        time.sleep(10)
        movies = json.loads(urllib2.urlopen('http://api.themoviedb.org/3/discover/movie?primary_release_date.gte=2017-12-01&primary_release_date.lte=2017-12-31&api_key=606aaffd7ca10f0b80804a1f0674e4e1').read())
 
    url = 'http://api.themoviedb.org/3/discover/movie?primary_release_date.gte=2017-12-01&primary_release_date.lte=2017-12-31&api_key=606aaffd7ca10f0b80804a1f0674e4e1&page='
    total_pages = movies['total_pages']

    result_movies = query(total_pages, url, 'title', 'release_date', 'movie', "Querying Movies:")

    return result_movies

def tv():
    try:
        tv = json.loads(urllib2.urlopen('http://api.themoviedb.org/3/discover/tv?first_air_date.gte=2017-12-01&first_air_date.lte=2017-12-31&api_key=606aaffd7ca10f0b80804a1f0674e4e1').read())
    except urllib2.HTTPError:
        time.sleep(10)
        tv = json.loads(urllib2.urlopen('http://api.themoviedb.org/3/discover/tv?first_air_date.gte=2017-12-01&first_air_date.lte=2017-12-31&api_key=606aaffd7ca10f0b80804a1f0674e4e1').read())

    url = 'http://api.themoviedb.org/3/discover/tv?first_air_date.gte=2017-12-01&first_air_date.lte=2017-12-31&api_key=606aaffd7ca10f0b80804a1f0674e4e1&page='
    total_pages = tv['total_pages']

    result_tv = query(total_pages, url, 'name', 'first_air_date', 'tv', "Querying TV Shows:")

    return result_tv

if __name__ == "__main__":
    
    result_movies = movies()

    result_tv = tv()

    result = compare(json.dumps(result_movies), json.dumps(result_tv))

    i = 0
    for k in result:
        i += 1

    print(str(i) + " Actors/Actresses appeared in at least 1 tv-show/movie in December of 2017!")

    response = raw_input('Would you like to see the output? Y/N: ')

    if response == "Y" or response == "y":
        print(json.dumps(result, indent=4))