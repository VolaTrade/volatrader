FROM alpine:3.12 as alpine

RUN apk add -U --no-cache ca-certificates

FROM scratch

COPY ./bin/volatrader /bin/volatrader 
COPY config.env . 

EXPOSE 8081

CMD ["/bin/volatrader"]
