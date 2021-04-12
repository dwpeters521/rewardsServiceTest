FROM node:latest

RUN mkdir /client
WORKDIR /client

ENV PATH /client/node_modules/.bin:$PATH

COPY package.json /package.json
COPY yarn.lock /yarn.lock
RUN yarn install
RUN yarn add typescript
RUN yarn global add react-scripts@4.0.3

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
