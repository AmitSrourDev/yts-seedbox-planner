import requests

def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

    return size
print("Starting.. make sure variables are defined")
file_name = "result.txt"
max_storage = 4*(2**40) #4tera
min_peers = 4
min_seeds = 15
target_quality = '1080p'
min_rating = 6
url = f'https://yts.mx/api/v2/list_movies.json?with_rt_ratings=true&minimum_rating={str(min_rating)}&limit=50&quality={target_quality}'
print(url)
json = requests.get(url).json()
file = open(file_name,"a", encoding='utf-8')
movie_count = json['data']['movie_count']
storage_count = 0

print(json['data']['movie_count'],'queries needed:',movie_count/50)
#print(json)
pages_needed = int(movie_count/50 ) +1

for i in range(1,pages_needed):
	print("page:",i,'/',pages_needed)
	json = requests.get(url+'&page='+str(i)).json()
	for movie in json['data']['movies']:
		#print(movie)
		for tor in movie['torrents']:
			#print(tor)
			if tor['quality'] == target_quality and tor['peers'] > min_peers and tor['seeds'] > min_seeds:
				storage_count = storage_count + tor['size_bytes']
				entry = f"Entry: {movie['title']} have {tor['seeds']}s/{tor['peers']}p takes {tor['size']} ({convert_bytes(tor['size_bytes'])} ) of {convert_bytes(storage_count)}/{convert_bytes(max_storage)} ({100*storage_count/max_storage }%)"
				print(entry)
				file.write(str(entry+'\n'))
				break

file.close()
