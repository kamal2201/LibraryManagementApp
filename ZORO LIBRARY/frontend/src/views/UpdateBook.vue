<template>
    <NavBar />
    <div class="background-image"></div>
    <div class="container mt-5">
      <h2 class="text-center mb-4">Update Book</h2>
      <form @submit.prevent="updateBook">
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input v-model="name" type="text" class="form-control" id="name" required>
        </div>
        <div class="mb-3">
          <label for="author" class="form-label">Author</label>
          <input v-model="author" type="text" class="form-control" id="author" required>
        </div>
        <div class="mb-3">
          <label for="genre" class="form-label">Genre</label>
          <input v-model="genre" type="text" class="form-control" id="genre" required>
        </div>
        <div class="mb-3">
          <label for="section" class="form-label">Section</label>
          <select v-model="section_id" class="form-control" id="section" required>
            <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">Content</label>
          <textarea v-model="content" class="form-control" id="content" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update</button>
      </form>
    </div>
  </template>
  
  <script>
  import NavBar from '@/components/NavBar.vue';
  import UserMixin from '../mixins/userMixin';
  
  export default {
    components: {
      NavBar
    },
    mixins: [UserMixin],
    data() {
      return {
        name: '',
        author: '',
        genre: '',
        section_id: null, // Ensure it's null or the correct default value
        content: '',
        sections: []
      };
    },
    mounted() {
      const bookId = this.$route.params.id;
      this.fetchBook(bookId);
      this.fetchSections();
    },
    methods: {
      async fetchBook(bookId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/view_book/${bookId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          });
          const data = await response.json();
          if (response.ok) {
            this.name = data.name;
            this.author = data.author;
            this.genre = data.genre;
            this.section_id = data.section_id; // Ensure section_id is assigned correctly
            this.content = data.content;
          } else {
            alert(data.error);
          }
        } catch (error) {
          console.log(error);
        }
      },
      async fetchSections() {
        try {
          const response = await fetch('http://127.0.0.1:5000/section', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          });
          const data = await response.json();
          if (response.ok) {
            this.sections = data;
          } else {
            alert(data.error);
          }
        } catch (error) {
          console.log(error);
        }
      },
      async updateBook() {
        const bookId = this.$route.params.id;
        try {
          const response = await fetch(`http://127.0.0.1:5000/update_book/${bookId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({
              name: this.name,
              author: this.author,
              genre: this.genre,
              section_id: this.section_id, // Ensure section_id is sent correctly
              content: this.content
            })
          });
          const data = await response.json();
          if (response.ok) {
            alert(data.message);
            this.$router.push('/book');
          } else {
            alert(data.error);
          }
        } catch (error) {
          console.log(error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
  
  body {
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
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
  
  .container {
    width: 100%;
    max-width: 500px;
    margin: auto;
    padding: 25px;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  h2 {
    margin-bottom: 20px;
    font-weight: 700;
  }
  
  .form-group {
    margin-bottom: 15px;
    text-align: left;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 700;
  }
  
  input, select, textarea {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  button {
    width: 100%;
    padding: 10px;
    margin-top: 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  