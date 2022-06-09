#FROM mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04
FROM python:3.8

# python installs
COPY /pipeline/container/model  .
RUN pip install -r requirements.txt && rm requirements.txt

ENTRYPOINT ["./score_script.py"]