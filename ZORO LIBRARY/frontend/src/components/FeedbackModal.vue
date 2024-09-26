<template>
    <div v-if="isVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="$emit('close')">&times;</span>
        <h2>Give Feedback</h2>
        <textarea v-model="feedbackText" placeholder="Enter your feedback here..."></textarea>
        <button @click="submitFeedback">Submit</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FeedbackModal',
    props: {
      book: Object,
      isVisible: Boolean
    },
    data() {
      return {
        feedbackText: ''
      };
    },
    methods: {
      async submitFeedback() {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            console.error('Token not found in localStorage');
            return;
          }
  
          const response = await fetch('http://127.0.0.1:5000/feedback', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              book_id: this.book.id,
              feedback: this.feedbackText
            })
          });
  
          if (response.ok) {
            const data = await response.json();
            console.log('Feedback submitted successfully:', data);
            alert('Feedback submitted successfully');
            this.$emit('submit');
            this.$emit('close');
          } else {
            console.error('Failed to submit feedback:', response.statusText);
          }
        } catch (error) {
          console.error('Error submitting feedback:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    z-index: 1000;
  }
  
  .modal-content {
    background: #fff;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
    width: 500px;
  }
  
  textarea {
    width: 100%;
    height: 100px;
    margin-bottom: 20px;
    border-radius: 5px;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  