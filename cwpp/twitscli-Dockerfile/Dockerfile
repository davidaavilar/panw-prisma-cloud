FROM ubuntu:22.04
ENV TOKEN=""
ENV CONSOLE=""
RUN apt update -y && apt upgrade -y && apt update -y && apt-get install curl -y
RUN curl --progress-bar -L -k --header "authorization: Bearer $TOKEN" $CONSOLE > twistcli
RUN chmod a+x twistcli