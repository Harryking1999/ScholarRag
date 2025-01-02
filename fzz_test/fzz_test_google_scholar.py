from serpapi import google_scholar_search
search = google_scholar_search.GoogleScholarSearch({
    "q": "contrastive decoding", 
    "api_key": "ba30b10feae3f3b298a6664711b92fd3875f3e803a2ab9fc43dee32c55df3c28"
  })
result = search.get_dict()
# print(result)

f = open("tmp_fzz_direct_search_res.txt")
f.write(str(result))
f.close()