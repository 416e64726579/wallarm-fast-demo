FROM postman/newman
RUN apk --no-cache add curl
COPY ./wait-for.sh .
ENTRYPOINT ["newman", "run", "/etc/postman/collection.json", "--environment=/etc/postman/collection_env.json"]
