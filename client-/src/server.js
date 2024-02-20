const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = 5000;

app.use(bodyParser.json());

app.post('/process_image', (req, res) => {
  const base64String = req.body.image;
  
  // Decode base64 string and save it to a file
  const buffer = Buffer.from(base64String, 'base64');
  fs.writeFile('uploaded_image.jpg', buffer, (err) => {
    if (err) {
      console.error('Error saving image:', err);
      res.status(500).json({ message: 'Error saving image.' });
    } else {
      console.log('Image saved successfully.');
      res.status(200).json({ message: 'Image saved successfully.' });
    }
  });
});

app.get('/get_processed_image', async (req, res) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/get_processed_image');
    if (response.ok) {
      const data = await response.json();
      const processedBase64Image = data.processed_image;

      // Decode Base64 to image buffer
      const imageBuffer = Buffer.from(processedBase64Image, 'base64');

      // Write the image buffer to a file
      fs.writeFile('processed_image.jpg', imageBuffer, (err) => {
        if (err) {
          console.error('Error writing processed image:', err);
          res.status(500).json({ message: 'Error writing processed image' });
        } else {
          console.log('Processed image saved successfully');
          res.sendFile('processed_image.jpg', { root: __dirname });
        }
      });
    } else {
      res.status(500).json({ message: 'Failed to retrieve processed image' });
    }
  } catch (error) {
    console.error('Error retrieving processed image:', error);
    res.status(500).json({ message: 'An error occurred while retrieving processed image' });
  }
});


app.listen(port, () => {
  console.log(`Server is running on http://127.0.0.1:5000`);
});
