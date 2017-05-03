FROM node:6.10.2
LABEL "maintainer" "Tony Lechner <tony@tony-lechner.com>"

ADD . /usr/src/app

WORKDIR /usr/src/app
CMD /usr/bin/env node /usr/src/app/lib/server/index.js
