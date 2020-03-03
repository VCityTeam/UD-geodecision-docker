# Start out of Miniconda (Anaconda Python) container as provide by Docker Hub
# (refer to https://hub.docker.com/r/continuumio/miniconda3)
FROM continuumio/miniconda3

# Install unzip to manage the files that will be downloaded
RUN apt-get install unzip

# Retrieve UD-geodecision's code (some git credentials are expected)
ARG git_token
RUN git clone https://$git_token@github.com/VCityTeam/UD-geodecision.git

# Make outputs directory
RUN mkdir outputs

# Retrieve the socio-eco data (GeoJSON file) from NextCloud server, and prepare them
RUN mkdir data
RUN wget https://box.liris.cnrs.fr/s/D2mdyEJa6coN3pX/download && unzip download -d /data && rm download

# Create conda virtual environment and install geodecision
# refer to
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually
#  - https://pythonspeed.com/articles/activate-conda-dockerfile/)

RUN conda env create -f ./UD-geodecision/geodecision/env.yml

# Remove .git directory
RUN rm -r ./UD-geodecision/.git

# The code to run when container is started:
COPY classify.py .
COPY entrypoint.py .
ENTRYPOINT ["python", "/entrypoint.py"]
