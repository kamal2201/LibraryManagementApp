<template>
    <div class="view-section-container">
      <NavBar />
      <div class="background-image"></div>
      <div class="container">
        <br>
        <h2><em>Books in {{ section.name }}</em></h2>
        <br>
        <div class="books-grid">
          <div v-for="book in books" :key="book.id" class="book-card">
            <h3>{{ book.name }}</h3>
            <p><strong>Author:</strong> {{ book.author }}</p>
            <p><strong>Genre:</strong> {{ book.genre }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NavBar from '@/components/NavBar.vue';
  
  export default {
    components: {
      NavBar
    },
    data() {
      return {
        books: [],
        section: {}
      };
    },
    created() {
      this.fetchSectionAndBooks();
    },
    methods: {
      async fetchSectionAndBooks() {
        try {
          const sectionId = this.$route.params.sectionId;
          const response = await fetch(`http://127.0.0.1:5000/view_section/${sectionId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          });
  
          const data = await response.json();
          if (response.ok) {
            this.section = data.section;
            this.books = data.books;
          } else {
            alert("Failed to fetch section and books");
          }
        } catch (error) {
          console.error('Error fetching section and books:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    padding: 20px;
  }
  
  .books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  
  .book-card {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 16px;
    text-align: left;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }
  
  .book-card h3 {
    margin: 0 0 10px;
  }
  
  .book-card p {
    margin: 0 0 10px;
  }
  
  .background-image {
    background-image: url('../assets/background.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -1;
  }
  </style>
  