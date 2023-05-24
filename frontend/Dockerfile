FROM node:18
WORKDIR /work

COPY package*.json ./
COPY yarn.lock ./
RUN yarn

CMD ["yarn", "dev", "--host"]
