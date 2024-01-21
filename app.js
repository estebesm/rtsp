const express = require('express');
const { createServer } = require('http');
const RTSPStream = require('node-rtsp-stream');

const app = express();
const server = createServer(app);

// Set up a static route to serve the static image
app.use('/static', express.static('static'));

// Set up RTSP stream
const rtspStream = new RTSPStream({
  name: 'test-stream',
  streamUrl: '/test',
  wsPort: 9999, // Use a different port for WebSocket
});

// Define a static image path
const staticImagePath = './images/1.jpg';

// Set the static image as the RTSP stream source
rtspStream.mpeg1Muxer.createReadStream = function () {
  return fs.createReadStream(staticImagePath);
};

// Start the Express server
const port = 3000;
server.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
