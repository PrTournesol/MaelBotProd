FROM debian:stretch
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install urllib3
RUN pip3 install ics
RUN pip3 install telepot
RUN pip3 install requests
# add credentials on build
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa
RUN chown -R root:root /root/.ssh
# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan -p 222 github.com >> /root/.ssh/known_hosts
#Problème de timezone
ENV TZ Europe/Paris
RUN cp /usr/share/zoneinfo/Europe/Paris /etc/localtime

#Prevent docker cache
ADD https://time.is/ /tmp/bustcache
RUN git clone git@github.com:PrTournesol/MaelBotProd.git

CMD python3 TelegramBot/bot.py 
