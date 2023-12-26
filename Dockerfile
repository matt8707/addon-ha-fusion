ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
  nodejs-current \
  npm \
  git

# remote
RUN git clone https://github.com/matt8707/ha-fusion /rootfs
RUN rm -rf /rootfs/data/*
WORKDIR /rootfs

# # local
# COPY rootfs /

RUN npm install --verbose
RUN npm run build --no-cache
RUN npm prune --omit=dev

RUN ln -s build/client/themes /themes
RUN ln -s /rootfs/data /data

ENV PORT 5050
ENV NODE_ENV=production

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
