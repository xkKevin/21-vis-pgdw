### installation
1. clone codes
2. deploy
    * ```shell
      export KUBECTL_BASE_URL=https://resource.static.zjvis.net/binary/kubectl \
          && export HELM_BASE_URL=https://resource.static.zjvis.net/binary/helm \
          && export IMAGE_BASE_URL=https://resource.static.zjvis.net/docker-images/app \
          && ./gradlew :deploy:deploy
      ```
3. upgrade