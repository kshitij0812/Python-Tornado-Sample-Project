### Getting started

##### 1. Install Requirements 
```
pip install -r requirements.txt
```

##### 2. Before starting the app server, update the value of these variable in ".env" file
- DB_USER
- DB_PASS
- DB_HOST
- DB_NAME
- DB_PORT

##### 3. Generate Database Tables
After running the below command tables will be cerated.
```
python util/createTables.py
```

##### 4. Start Server
```
python app.py -p 8003
```

Now if you go to [http://127.0.0.1:8003](http://127.0.0.1:8003), you'll see the Generate New Book Page
