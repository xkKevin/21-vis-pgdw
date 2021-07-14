# flask_vue_template

## Front-End

### Project setup
```
npm install
```

#### Compiles and hot-reloads for development
```
npm run serve
```

#### Compiles and minifies for production
```
npm run build
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


## Back-End

### Project setup
```
pip install -r backend\requirements.txt 
# if you want to use image sources to speed up installation:
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r backend\requirements.txt 
```

### Run the project
```
python backend\app.py
```


##### Others
`kubectl cp ./generate_transform_specs.py pgdw-78b459fb4-nj9f6:/PG4DT/backend/generate_transform_specs.py`
Use `https://morpheus.projects.zjvis.org/useMorpheus?caseString=benchmarks/1/r1_input1.csv|benchmarks/1/r1_output1.csv` to test whether the Morpheus Server is running.
