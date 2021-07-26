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

+ Java
+ Docker

##### Run

+ `./gradlew :morpheus:runDockerImage`
+ `./gradlew :backend:runDockerImage`
+ `./gradlew :frontend:runDockerImage`
    + http://localhost:8888

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

##### Frontend

+ node

##### Morpheus

See https://utopia-group.github.io/morpheus/ for more details.