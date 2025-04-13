import requests

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQ2NjcwLCJpYXQiOjE3NDQ1NjAyNzAsImp0aSI6Ijg4MTBmMDQ2ZTNiYjQzMGZiYmI1YTk4YmIyZGM3ZjExIiwidXNlcl9pZCI6MTl9.kr1dQ27AJffUz5LFZ5MhQICyeKYzbn8hZ6OZUYQXNA4'  # replace with your real token
}

response = requests.get('http://localhost:8000/api/favorite-garages/', headers=headers)
print(response.json())
