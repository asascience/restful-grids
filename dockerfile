FROM mambaorg/micromamba:latest

RUN --mount=type=cache,id=mamba,target=/opt/conda/pkgs,uid=1000,gid=1000 \
    --mount=type=bind,source=environment.yml,target=/tmp/environment.yml \
    micromamba install -y -n base -f /tmp/environment.yml

EXPOSE 9005
COPY . .
WORKDIR xpublish

#ENTRYPOINT ["python" "uvicorn" "--port" "9005" "main:app" "--reload"]
#CMD ["uvicorn" "--port" "9005" "main:app" "--reload"]
CMD python main.py