package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"image"
	_ "image/png"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

type CaptchaSolver struct {
	TesseractPath string
	ModelPath     string
}

type CaptchaResult struct {
	Success bool   `json:"success"`
	Text    string `json:"text"`
	Method  string `json:"method"`
}

func NewCaptchaSolver() *CaptchaSolver {
	return &CaptchaSolver{
		TesseractPath: "tesseract",
		ModelPath:     "./models/",
	}
}

func (cs *CaptchaSolver) SolveImage(imageData []byte) (*CaptchaResult, error) {
	// Try OCR first
	if result, err := cs.solveWithOCR(imageData); err == nil && result.Success {
		return result, nil
	}

	// Try pattern matching
	if result, err := cs.solveWithPatterns(imageData); err == nil && result.Success {
		return result, nil
	}

	// Try ML model
	return cs.solveWithML(imageData)
}

func (cs *CaptchaSolver) solveWithOCR(imageData []byte) (*CaptchaResult, error) {
	tmpFile := fmt.Sprintf("/tmp/captcha_%d.png", time.Now().UnixNano())
	defer os.Remove(tmpFile)

	if err := os.WriteFile(tmpFile, imageData, 0644); err != nil {
		return nil, err
	}

	cmd := exec.Command(cs.TesseractPath, tmpFile, "stdout", "-c", "tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
	output, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	text := strings.TrimSpace(string(output))
	if len(text) > 0 {
		return &CaptchaResult{
			Success: true,
			Text:    text,
			Method:  "OCR",
		}, nil
	}

	return &CaptchaResult{Success: false}, nil
}

func (cs *CaptchaSolver) solveWithPatterns(imageData []byte) (*CaptchaResult, error) {
	// Load image
	img, _, err := image.Decode(bytes.NewReader(imageData))
	if err != nil {
		return nil, err
	}

	// Simple pattern matching for common captcha types
	bounds := img.Bounds()
	width, height := bounds.Max.X, bounds.Max.Y

	// Math captcha detection
	if width < 200 && height < 100 {
		if text := cs.solveMathCaptcha(imageData); text != "" {
			return &CaptchaResult{
				Success: true,
				Text:    text,
				Method:  "Math",
			}, nil
		}
	}

	return &CaptchaResult{Success: false}, nil
}

func (cs *CaptchaSolver) solveMathCaptcha(imageData []byte) string {
	// Simple math captcha solver
	cmd := exec.Command(cs.TesseractPath, "-", "stdout", "-c", "tessedit_char_whitelist=0123456789+-=x*")
	cmd.Stdin = bytes.NewReader(imageData)
	output, err := cmd.Output()
	if err != nil {
		return ""
	}

	text := strings.TrimSpace(string(output))
	if strings.Contains(text, "+") || strings.Contains(text, "-") || strings.Contains(text, "*") {
		// Parse and solve simple math
		return cs.evaluateMath(text)
	}

	return ""
}

func (cs *CaptchaSolver) evaluateMath(expr string) string {
	// Basic math evaluation
	expr = strings.ReplaceAll(expr, " ", "")
	if strings.Contains(expr, "+") {
		parts := strings.Split(expr, "+")
		if len(parts) == 2 {
			var a, b int
			if n1, _ := fmt.Sscanf(parts[0], "%d", &a); n1 == 1 {
				if n2, _ := fmt.Sscanf(parts[1], "%d", &b); n2 == 1 {
					return fmt.Sprintf("%d", a+b)
				}
			}
		}
	}
	return ""
}

func (cs *CaptchaSolver) solveWithML(imageData []byte) (*CaptchaResult, error) {
	// Placeholder for ML model integration
	return &CaptchaResult{Success: false}, nil
}

func (cs *CaptchaSolver) SolveAudio(audioData []byte) (*CaptchaResult, error) {
	// Audio captcha solver using speech recognition
	tmpFile := fmt.Sprintf("/tmp/audio_%d.wav", time.Now().UnixNano())
	defer os.Remove(tmpFile)

	if err := os.WriteFile(tmpFile, audioData, 0644); err != nil {
		return nil, err
	}

	// Use speech recognition (requires additional setup)
	return &CaptchaResult{Success: false}, nil
}

func main() {
	solver := NewCaptchaSolver()
	
	http.HandleFunc("/solve", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			http.Error(w, "Method not allowed", 405)
			return
		}

		var req struct {
			Image string `json:"image"`
			Type  string `json:"type"`
		}

		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid JSON", 400)
			return
		}

		imageData, err := base64.StdEncoding.DecodeString(req.Image)
		if err != nil {
			http.Error(w, "Invalid base64", 400)
			return
		}

		result, err := solver.SolveImage(imageData)
		if err != nil {
			http.Error(w, err.Error(), 500)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(result)
	})

	fmt.Println("Captcha solver running on :8080")
	http.ListenAndServe(":8080", nil)
}