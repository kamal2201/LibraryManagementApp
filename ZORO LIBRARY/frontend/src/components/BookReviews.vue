<template>
    <div v-if="isVisible" class="modal-overlay">
      <div class="modal-content">
        <h3>Reviews for Book ID: {{ bookId }}</h3>
        <button class="btn btn-close" @click="$emit('close')">Close</button>
        <div class="reviews-container">
          <div v-if="reviews.length">
            <div v-for="review in reviews" :key="review.id" class="review-item">
              <p><strong>User:</strong> {{ review.user_mail }}</p>
              <p><strong>Feedback:</strong> {{ review.feedback }}</p>
            </div>
          </div>
          <div v-else>
            <p>No reviews available for this book.</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      bookId: Number,
      isVisible: Boolean
    },
    data() {
      return {
        reviews: []
      };
    },
    watch: {
      bookId: 'fetchReviews'
    },
    methods: {
      async fetchReviews() {
        if (!this.bookId) return;
        try {
          const token = localStorage.getItem('access_token');
          const response = await fetch(`http://127.0.0.1:5000/reviews/${this.bookId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
          const data = await response.json();
          if (response.ok) {
            this.reviews = data;
          } else {
            console.error('Failed to fetch reviews:', data.error);
          }
        } catch (error) {
          console.error('Error fetching reviews:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 80%;
    max-width: 600px;
    position: relative;
    max-height: 80vh; /* Limit height to fit on screen */
    overflow: hidden; /* Hide overflow for scrolling */
  }
  
  .reviews-container {
    max-height: 60vh; /* Adjust height as needed */
    overflow-y: auto; /* Enable vertical scrolling */
    padding-right: 10px; /* To avoid scrollbar overlap */
  }
  
  .btn-close {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .review-item {
    margin-bottom: 15px;
  }
  </style>
  