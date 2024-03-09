### Somnus

#### Introduction

In this work, we explore visualization designs for depicting the semantics of code pieces in the context of data transformation.

We design a pipeline, called SOMNUS, that visualizes the creation and evolution of data tables across a series of transformations.

SOMNUS accepts a data wrangling script with its source tables as input and results in a glyph-based provenance graph where nodes represent tables and edges denote data transformations. 

There are three modules in Somnus project: Backend, Frontend, and Morpheus.
See *Project Deployment* to setup Somnus.
See *Development* to test and add new features.

#### Project Deployment

##### Environment

+ JDK 1.8 (Java SE 8)
  + [Download](https://www.oracle.com/java/technologies/javase/javase8u211-later-archive-downloads.html)
+ Docker

##### Run

Run modules separately:
+ `./gradlew :morpheus:runDockerImage` for Morpheus
  + <http://localhost:8890>
+ `./gradlew :backend:runDockerImage` for Backend
  + <http://localhost:8889>
+ `./gradlew :frontend:runDockerImage` for Frontend
  + <http://localhost:8888>

You can also run all modules in one command:
+ `./gradlew runDockerImage`
    + <http://localhost:8888>

Kill all containers in one command:
+ `./gradlew killDockerContainer`

#### Development

##### Backend

+ Python 3.7
  + Flask
  + Pandas
  + requests
  + See `backend/requirements.txt` for details.
  + Run `pip install -r backend/requirements.txt` to install these packages.
    + You can use image sources to speed up this installation process, such as `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r backend/requirements.txt`  
+ R 4.1
  + dplyr
  + tydir

RUN: `python backend/src/app.py`

##### Frontend

+ node: v16.4.2

RUN:
  + `cd frontend`
  + `npm install`
    + We use `https://registry.npm.taobao.org/` as our nmp Registry. If you want to change it, you can remove `.npmrc` and run `npm config set registry http://registry.npmjs.org/`.
  + `npm run serve`

##### Morpheus

See https://utopia-group.github.io/morpheus/ for more details.

#### Reference
K. Xiong, S. Fu, G. Ding, Z. Luo, R. Yu, W. Chen, H. Bao, and Y. Wu. Visualizing the Scripts of Data Wrangling With SOMNUS. *IEEE Transactions on Visualization and Computer Graphics*, 29(6):2950–2964, 2023. doi: 10.1109/TVCG.2022.3144975 