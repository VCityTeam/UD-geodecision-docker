### Building and running instructions: the shell way
The docker build process requires access to the [UD-geodecision github repository](https://github.com/VCityTeam/UD-geodecision).
In order to transmit such credentials to the building process you should
first [create a personnal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) (referenced as `TOKEN` below).

Note that when required to [specify the token scopes](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) you apprently need to select `repo` in order to allow for cloning.

Once you have a `TOKEN` launch the following command:
```bash
docker build --build-arg git_token=<TOKEN> -t liris/geodecision DockerContext
```
You can now run the container with
```bash
docker run --mount src=`pwd`,target=/Input,type=bind --mount src=`pwd`,target=/Output,type=bind --rm -it liris/geodecision 
```
The outputs are placed in `data/outputs` subdirectory.

### Developer's notes
 * In order to debug the build container use
   ```bash
   docker run --entrypoint /bin/bash -it liris/geodecision 
   ```

