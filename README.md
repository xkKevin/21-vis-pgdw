### Somnus

#### Introduction

In this work, we explore visualization design for depicting the semantics of code pieces in the context of data transformation.
In this system our design space consisting of two dimensions that guide the design of a collection of 23 glyphs
We designed a pipeline, called SOMNUS, that visualizes the creation and evolution of data tables across a series of transformations
We have three modules for our Somnus project: Backend, Frontend, and Morpheus.
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
  + See `path to requirements.txt`
+ R 4.1
  + dplyr
  + tydir

RUN: `python backend/src/app.py`

##### Frontend

+ node

RUN:
  + `cd frontend`
  + `npm install`
  + `npm run serve`

##### Morpheus

See https://utopia-group.github.io/morpheus/ for more details.