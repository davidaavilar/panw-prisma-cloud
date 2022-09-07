FROM nginx:1.19.10
USER root
RUN useradd -ms /bin/bash nginxuser
USER nginxuser # changed to nginxuser
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]