# Start out of Miniconda (Anaconda Python) container as provide by Docker Hub
# (refer to https://hub.docker.com/r/continuumio/miniconda3)
FROM continuumio/miniconda3

# Make outputs directory
RUN mkdir outputs

# Retrieve UD-geodecision's code (some git credentials are expected)
ARG git_token
RUN git clone https://$git_token@github.com/VCityTeam/UD-geodecision.git

# Create conda virtual environment and install geodecision
# refer to
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
#  - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually
#  - https://pythonspeed.com/articles/activate-conda-dockerfile/)

RUN conda env create -f ./UD-geodecision/geodecision/env.yml

# The code to run when container is started:
COPY get_graph.py .
COPY entrypoint.py .
ENTRYPOINT ["python", "/entrypoint.py"]
