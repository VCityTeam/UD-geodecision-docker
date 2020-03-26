# Start out of Miniconda (Anaconda Python) container as provide by Docker Hub
# (refer to https://hub.docker.com/r/continuumio/miniconda3)
FROM continuumio/miniconda3

# Create conda virtual environment: refer to
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually
#  - https://pythonspeed.com/articles/activate-conda-dockerfile/)
RUN apt-get install unzip

# Retrieve the CityGML files from NextCloud server, and prepare them
RUN mkdir data
RUN mkdir /data/outputs
RUN wget https://box.liris.cnrs.fr/s/S6pxYb4kEmzCFgt/download && unzip download -d /data && rm download

# Retrieve UD-geodecision's code (some git credentials are expected)
ARG git_token
RUN git clone https://$git_token@github.com/VCityTeam/UD-geodecision.git

# Create a directory channel
RUN mkdir -p /tmp/my-conda-channel/linux-64

# Copy the build file to the channel & architecture directory
RUN cp UD-geodecision/geodecision/conda.build/linux-64/geodecision-0.1-0.tar.bz2 /tmp/my-conda-channel/linux-64/
RUN conda install conda-build 

# Index the channel
RUN conda index /tmp/my-conda-channel/linux-64/

# Create conda virtual environment
RUN conda create --name geodecision
SHELL ["conda", "run", "-n", "geodecision", "/bin/bash", "-c"]

# Conda install geodecision package
RUN conda config --append channels conda-forge
RUN conda install -c file://tmp/my-conda-channel/ geodecision=0.1

# Remove .git directory
RUN rm -r ./UD-geodecision/.git

# The code to run when container is started:
COPY get_analysed_roofs.py .
COPY entrypoint.py .
ENTRYPOINT ["python", "/entrypoint.py"]
