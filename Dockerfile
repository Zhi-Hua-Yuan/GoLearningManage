FROM golang:1.27.2 AS build

WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/learning-manage-api ./cmd/api

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/learning-manage-api /learning-manage-api
EXPOSE 8123
USER nonroot:nonroot
ENTRYPOINT ["/learning-manage-api"]