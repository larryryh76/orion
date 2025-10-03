FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip golang-go curl wget \
    chromium-browser xvfb libssl-dev pkg-config && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt flask flask-cors
RUN go mod tidy && go build -o captcha_solver captcha_solver.go
RUN cargo build --release

EXPOSE 5000 8080
CMD ["python3", "cloud_server.py"]