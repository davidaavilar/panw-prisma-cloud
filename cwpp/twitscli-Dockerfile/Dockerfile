FROM ubuntu:18.04
RUN apt update -y && apt upgrade -y && apt update -y && apt-get install curl -y
RUN curl -V --progress-bar -L -k --header "authorization: Bearer $TOKEN" $CONSOLE/api/v1/util/twistcli > twistcli
RUN chmod a+x twistcli