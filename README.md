# Network Monitor Intrusion Model

This project is a network monitor intrusion model that uses machine learning to analyze network traffic and detect potential intrusions. The model is built using TensorFlow and Keras, and the application is developed using Flask and Flask-RESTful.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/youssef-faik/network-monitor-intrusion-model.git
   cd network-monitor-intrusion-model
   ```

2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

## Usage

1. Start the Flask application:
   ```bash
   docker-compose up
   ```

2. Send a POST request to the `/analyze` endpoint with the network traffic data in JSON format. For example:
   ```bash
   curl -X POST http://localhost:5000/analyze -H "Content-Type: application/json" -d '[
       {
           "flowDuration": 12345,
           "protocol": "TCP",
           "sourceIp": "192.168.1.1",
           "destinationIp": "192.168.1.2",
           "sourcePort": 1234,
           "destinationPort": 80,
           "packetLength": 100,
           "totalBytes": 1000
       }
   ]'
   ```

3. The response will contain the analysis results.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch to your fork.
4. Create a pull request with a description of your changes.

