<template>
  <NavBar />
  <div class="background-image"></div>
  <div class="container">
    <br>
    <h2><em>All Books</em></h2>
    <div class="top-actions">
      <router-link v-if="isloggedin && email === 'librarian@gmail.com'" to="/create_book" class="btn btn-dark">Add Book</router-link>
    </div>
    <div class="sections-grid">
      <div v-for="book in books" :key="book.id" class="section-card">
        <img v-if="book.coverImage" :src="book.coverImage" alt="Book Cover" class="book-cover" />
        <h3>{{ book.name }}</h3>
        <p>Author: {{ book.author }}</p>
        <p>Genre: {{ book.genre }}</p>
        <div class="button-group">
          <router-link v-if="isloggedin && email === 'librarian@gmail.com'" :to="`/update_book/${book.id}`" class="btn btn-update">Update</router-link>
          <button v-if="isloggedin && email !== 'librarian@gmail.com'" @click="requestBook(book.id)" class="btn btn-update">Request</button>
          <button v-if="isloggedin && email !== 'librarian@gmail.com'" @click="openReviewsModal(book.id)" class="btn btn-update">Reviews</button>
          <button v-if="isloggedin && email === 'librarian@gmail.com'" @click="deleteBook(book.id)" class="btn btn-delete">Delete</button>
        </div>
      </div>
    </div>
    <BookReviews :bookId="selectedBookId" :isVisible="isReviewsModalVisible" @close="closeReviewsModal" />
    <br><br>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import BookReviews from '@/components/BookReviews.vue';
import UserMixin from '../mixins/userMixin';

export default {
  components: {
    NavBar,
    BookReviews
  },
  mixins: [UserMixin],
  data() {
    return {
      books: [],
      selectedBookId: null,
      isReviewsModalVisible: false
    };
  },
  created() {
    this.getBooks();
  },
  methods: {
    async getBooks() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          return alert('Access token is missing. Please log in again.');
        }

        const response = await fetch('http://127.0.0.1:5000/book', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        const data = await response.json();
        if (response.ok) {
          this.books = data;
        } else {
          alert("Something went wrong");
        }
      } catch (error) {
        console.log(error);
      }
    },

    async deleteBook(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/delete_book/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.getBooks();
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.log(error);
      }
    },

    async requestBook(bookId) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('Access token is missing. Please log in again.');
          return;
        }

        const response = await fetch(`http://127.0.0.1:5000/request_book/${bookId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error('Error requesting book:', error);
      }
    },

    openReviewsModal(bookId) {
      this.selectedBookId = bookId;
      this.isReviewsModalVisible = true;
    },

    closeReviewsModal() {
      this.isReviewsModalVisible = false;
      this.selectedBookId = null;
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
}

.top-actions {
  margin-top: 5%;
  margin-bottom: 3%;
}

.btn {
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-decoration: none;
  text-align: center;
}

.btn-dark {
  background-color: #343a40;
}

.btn-view {
  background-color: rgb(196, 135, 250); 
}

.btn-update {
  background-color: orange; 
}

.btn-delete {
  background-color: #dc3545;
}

.btn:hover {
  opacity: 0.8;
}

.sections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.section-card {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.section-card h3 {
  margin: 0 0 10px;
}

.section-card p {
  margin: 0 0 20px;
}

.button-group {
  display: flex;
  justify-content: space-around;
}

.button-group button,
.button-group a {
  border: none;
  color: white;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.button-group button:hover,
.button-group a:hover {
  opacity: 0.8;
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

.book-cover {
  max-width: 100%;
  height: auto;
  margin: 0 auto 10px auto;
  display: block;
  object-fit: cover;
  width: 150px;
  height: 200px;
}
</style>
