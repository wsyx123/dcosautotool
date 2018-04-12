FROM nginx-django1.11
COPY dcosauto /dcosauto
ENTRYPOINT ["/dcosauto/start.sh"]

