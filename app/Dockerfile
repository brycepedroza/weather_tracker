FROM node:13.1-alpine as build

ARG REACT_APP_ENV=local

WORKDIR /usr/src/app
COPY package.json ./
COPY yarn.lock ./
RUN yarn cache clean && yarn --update-checksums
COPY . ./
RUN yarn && yarn build

# Stage - Production
FROM node:13.1-alpine
RUN yarn global add serve
WORKDIR /user/src/app
COPY --from=build /usr/src/app/build .
CMD ["serve", "-p", "4000", "-s", "."]
