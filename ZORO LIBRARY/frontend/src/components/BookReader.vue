<template>
    <div class="book-reader-overlay" v-if="isVisible">
      <div class="book-reader">
        <button @click="closeReader" class="close-button">&times;</button>
        <h2>{{ book.name }}</h2>
        <p>Author: {{ book.author }}</p>
        <p>Genre: {{ book.genre }}</p>
        <div class="book-content">
          <!-- Display the content of the book here -->
          <p>{{ book.content }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BookReader',
    props: {
      book: {
        type: Object,
        required: true
      },
      isVisible: {
        type: Boolean,
        required: true
      }
    },
    methods: {
      closeReader() {
        this.$emit('close');
      }
    }
  };
  </script>
  
  <style scoped>
  .book-reader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .book-reader {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 80%;
    max-width: 600px;
    max-height: 80%;
    overflow-y: auto;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    position: relative; /* Ensure the close button is positioned correctly */
  }
  
  .close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }
  
  .book-content {
    margin-top: 20px;
    max-height: 60vh; 
    overflow-y: auto; 
  }
  </style>
  