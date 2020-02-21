# Start out of Miniconda (Anaconda Python) container as provide by Docker Hub
# (refer to https://hub.docker.com/r/continuumio/miniconda3)
FROM continuumio/miniconda3

# Create conda virtual environment: refer to
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually
#  - https://pythonspeed.com/articles/activate-conda-dockerfile/)
RUN apt-get install unzip
COPY env.yml .
RUN conda env create -f env.yml

# Retrieve the CityGML files from NextCloud server, and prepare them
RUN mkdir data
RUN mkdir /data/outputs
#RUN wget https://box.liris.cnrs.fr/s/S6pxYb4kEmzCFgt/download && unzip download -d /data && rm download
RUN wget https://box.liris.cnrs.fr/s/RpLmwooKtXzSmCR/download && unzip download -d /data && rm download

# Retrieve UD-geodecision's code (some git credentials are expected)
ARG git_token
RUN git clone https://$git_token@github.com/VCityTeam/UD-geodecision.git
RUN mv UD-geodecision/geodecision/geodecision .
# Replace above line with
# RUN cd UD-geodecision/geodecision && pip install . && cd ../..

# The code to run when container is started:
COPY get_analysed_roofs.py .
COPY entrypoint.py .
ENTRYPOINT ["python", "/entrypoint.py"]
