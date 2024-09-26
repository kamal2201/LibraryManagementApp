<template>
  <div class="my-books-container">
    <NavBar />
    <div class="background-image"></div>
    <div class="container">
      <br>
      <h2><em>My Approved Books</em></h2>
      <div class="books-grid">
        <div v-for="(book, index) in approvedBooks" :key="index" class="book-card">
          <h3>{{ book.name }}</h3>
          <p><strong>Author:</strong> {{ book.author }}</p>
          <p><strong>Genre:</strong> {{ book.genre }}</p>
          <div class="button-group">
            <button @click="openBookReader(book)" class="btn btn-view">Read</button>
            <button @click="openFeedbackModal(book)" class="btn btn-feedback">Review</button>
            <button @click="returnBook(book.id)" class="btn btn-return">Return</button>
          </div>
        </div>
      </div>
      <div v-if="approvedBooks.length === 0" class="no-books-message">
        <p>No approved books found.</p>
      </div>
    </div>
    <BookReader :book="selectedBook" :isVisible="isReaderVisible" @close="closeBookReader" />
    <FeedbackModal :book="selectedBook" :isVisible="isFeedbackModalVisible" @submit="submitFeedback" @close="closeFeedbackModal" />
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';
  import BookReader from '@/components/BookReader.vue';
  import FeedbackModal from '@/components/FeedbackModal.vue';
  import UserMixin from '../mixins/userMixin';

  export default {
    name: 'MyBooks',
    components: {
      NavBar,
      BookReader,
      FeedbackModal
    },
    mixins: [UserMixin],
    data() {
      return {
        approvedBooks: [],
        selectedBook: null,
        isReaderVisible: false,
        isFeedbackModalVisible: false
      };
    },
    created() {
      this.fetchApprovedBooks();
    },
    methods: {
      async fetchApprovedBooks() {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            console.error('Token not found in localStorage');
            return;
          }

          const response = await fetch('http://127.0.0.1:5000/my_books', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });

          if (response.ok) {
            const data = await response.json();
            console.log('Fetched data:', data);
            this.approvedBooks = data;
          } else {
            console.error('Failed to fetch approved books:', response.statusText);
          }
        } catch (error) {
          console.error('Error fetching approved books:', error);
        }
      },

      openBookReader(book) {
        this.selectedBook = book;
        this.isReaderVisible = true;
      },

      closeBookReader() {
        this.isReaderVisible = false;
        this.selectedBook = null;
      },

      openFeedbackModal(book) {
        this.selectedBook = book;
        this.isFeedbackModalVisible = true;
      },

      closeFeedbackModal() {
        this.isFeedbackModalVisible = false;
        this.selectedBook = null;
      },

      async returnBook(bookId) {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            console.error('Token not found in localStorage');
            return;
          }

          const response = await fetch(`http://127.0.0.1:5000/return_book/${bookId}`, {
            method: 'PUT',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              is_returned: true,
              is_approved: false
            })
          });

          if (response.ok) {
            const data = await response.json();
            console.log('Book returned successfully:', data);
            alert('Book returned successfully');
            this.fetchApprovedBooks(); // Refresh the list after returning the book
          } else {
            console.error('Failed to return book:', response.statusText);
          }
        } catch (error) {
          console.error('Error returning book:', error);
        }
      },

      handleFeedbackSubmit(bookId) {
        this.returnBook(bookId);
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
}

.book-card {
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

.book-card h3 {
  margin: 0 0 10px;
}

.book-card p {
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

.button-group button.btn-view {
  background-color: rgb(196, 135, 250);
}

.button-group button.btn-feedback {
  background-color: #4caf50;
}

.button-group button.btn-return {
  background-color: #ff9800;
}

.button-group button:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

.no-books-message {
  text-align: center;
  margin-top: 20px;
  font-size: 1.1em;
  color: #777;
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
  opacity: 1; /* Adjust opacity to make the background visible */
}
</style>
