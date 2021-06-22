FROM python:3.9

ENV \
  # This prevents Python from writing out pyc files \
  PYTHONDONTWRITEBYTECODE=1 \
  # This keeps Python from buffering stdin/stdout \
  PYTHONUNBUFFERED=1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /code

ENTRYPOINT ["/entrypoint"]
