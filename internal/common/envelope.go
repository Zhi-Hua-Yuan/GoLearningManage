package common

// Envelope is the wire-compatible response envelope used by every public API.
type Envelope[T any] struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
	Data    T      `json:"data"`
}

func Success[T any](data T) Envelope[T] {
	return Envelope[T]{Code: 0, Message: "ok", Data: data}
}
