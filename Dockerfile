FROM python:3-bookworm

RUN apt-get update && \
    apt-get install -y libmagickwand-dev ghostscript fonts-freefont-ttf curl libgl1-mesa-glx
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app
COPY --chown=user . /app
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv sync
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "run.py"]
