<template>
    <div id="app">
      <header class="app-header">
        <h1>Facial Analysis</h1>
      </header>
      <div class="button"><button @click="processImage">Process Image</button></div> 
    <div class="container">
      <div class="left-section">
        <h2>Upload Image</h2>
        <input type="file" @change="uploadImage" ref="fileInput" />
        
        <div class="preview" v-if="imageUrl">
          <img :src="imageUrl" alt="Uploaded Image">
        </div>
      </div>
      
      
      <div class="right-section" v-if="processedImage">
        <h2>Processed Image</h2>
        <div v-if="isLoading">Loading...</div>
        <img class="processedImage" v-if="processedImage" :src="processedImage" alt="Processed Image" />
      </div>
    </div>
    <div>
      <footer class="app-footer">
        <p>Powered by <a href="Develop in 2024 ">BMW </a></p>
      </footer>
    </div>
  </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        imageUrl: null,
        apiBaseUrl: 'http://127.0.0.1:5000', // Replace with your Flask API URL
        isLoading: false,
        processedImage: null,
      };
    },
    methods: {
      uploadImage(event) {
        const file = event.target.files[0];
  
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.imageUrl = e.target.result; // Display preview 
          };
          reader.readAsDataURL(file);
        }
      },
      async processImage() {
        if (!this.imageUrl) return;
  
        try {
          const imageData = this.imageUrl.split(',')[1]; // Get base64 data (exclude header)
          const response = await axios.post(`${this.apiBaseUrl}/process`, { image: imageData });
  
          if (response.status === 200) {
            console.log("Image sent for processing successfully");
          } else {
            console.error("Unexpected status code from /process:", response.status);
          }
  
          this.isLoading = true;
          const getResponse = await axios.get(`${this.apiBaseUrl}/processed`);
  
          if (getResponse.data && getResponse.data.image) {
            console.log("Processed image received successfully");
            this.processedImage = 'data:image/jpeg;base64,' + getResponse.data.image; // 'data:image/jpeg;base64,....
  
          } else {
            console.error("Unexpected response from /processed:", getResponse.data);
          }
  
        } catch (error) {
          console.error("Image processing error:", error);
          // Handle the error, e.g., display an error message
        } finally {
          this.isLoading = false;
        }
      }
    },
  };
  </script>
  
  <style>
  /* Add basic styling for layout */
  .app-header {
    text-align: center;
    background-color: lightblue; /* Change background color to light blue */
  }
  .container {
    display: flex;
  }
  .left-section, .right-section {
    width: 50%;
    padding: 20px;
    border: 1px solid #000;
  
  }
  .preview img, .right-section img {
    max-width: 100%;
    border: 1px solid #000;
  }
  .app-footer {
    text-align: center;
    margin-top: 20px;
  }
  .button {
    text-align: center;
    margin-top: 20px;
  }
  .processedImage {
    padding-top: 20px;
    max-width: 100%;
    /* border: 1px solid #000; */
  }
  </style>