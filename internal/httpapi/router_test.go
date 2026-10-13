package httpapi_test

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"unicode/utf8"

	"github.com/Zhi-Hua-Yuan/GoLearningManage/internal/httpapi"
)

func TestHealthContract(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/api/health", nil)
	recorder := httptest.NewRecorder()

	httpapi.NewRouter().ServeHTTP(recorder, req)

	if recorder.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", recorder.Code, http.StatusOK)
	}
	if got := recorder.Header().Get("X-Trace-Id"); len(got) != 32 || !isLowerHex(got) {
		t.Fatalf("generated X-Trace-Id = %q, want 32 lowercase hexadecimal characters", got)
	}

	var body struct {
		Code    int    `json:"code"`
		Message string `json:"message"`
		Data    string `json:"data"`
	}
	if err := json.Unmarshal(recorder.Body.Bytes(), &body); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	if body.Code != 0 || body.Message != "ok" || body.Data != "ok" {
		t.Fatalf("body = %+v, want code=0 message=ok data=ok", body)
	}
}

func TestTraceIdIsPropagatedWhenValid(t *testing.T) {
	const traceID = "0123456789abcdef0123456789abcdef"
	req := httptest.NewRequest(http.MethodGet, "/api/health", nil)
	req.Header.Set("X-Trace-Id", traceID)
	recorder := httptest.NewRecorder()

	httpapi.NewRouter().ServeHTTP(recorder, req)

	if got := recorder.Header().Get("X-Trace-Id"); got != traceID {
		t.Fatalf("propagated X-Trace-Id = %q, want %q", got, traceID)
	}
}

func isLowerHex(value string) bool {
	for _, r := range value {
		if !utf8.ValidRune(r) || !((r >= '0' && r <= '9') || (r >= 'a' && r <= 'f')) {
			return false
		}
	}
	return true
}
