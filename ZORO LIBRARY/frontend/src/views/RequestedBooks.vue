<template>
  <div class="requested-books-container">
    <NavBar />
    <div class="background-image"></div>
    <div class="container">
      <br>
      <h2><em>Requested Books</em></h2>
      <div class="table-container">
        <table class="requested-books-table">
          <thead>
            <tr>
              <th>Book Name</th>
              <th>Genre</th>
              <th>Author</th>
              <th v-if="isloggedin && this.email === 'librarian@gmail.com'">User</th>
              <th v-if="isloggedin && this.email !== 'librarian@gmail.com'">Status</th>
              <th v-if="isloggedin && this.email === 'librarian@gmail.com'">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(request, index) in requestedBooks" :key="index">
              <td>{{ request.book.name }}</td>
              <td>{{ request.book.genre }}</td>
              <td>{{ request.book.author }}</td>
              <td v-if="isloggedin && this.email === 'librarian@gmail.com'">{{ request.user_mail }}</td>
              <td v-if="isloggedin && this.email !== 'librarian@gmail.com'">{{ getRequestStatus(request) }}</td>
              <td v-if="isloggedin && this.email === 'librarian@gmail.com' && request.is_requested">
                <button @click="acceptRequest(request.id)" class="btn btn-accept">Approve</button>
                <span class="button-gap"></span> <!-- Adding a span for spacing -->
                <button @click="rejectRequest(request.id)" class="btn btn-reject">Reject</button>
              </td>
              <td v-if="isloggedin && this.email === 'librarian@gmail.com' && !request.is_requested && !request.is_approved && !request.is_rejected">Returned</td>
              <td v-if="isloggedin && this.email === 'librarian@gmail.com' && request.is_approved">Approved</td>
              <td v-if="isloggedin && this.email === 'librarian@gmail.com' && request.is_rejected">Rejected</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
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
      requestedBooks: []
    }
  },
  created() {
    this.getRequestedBooks();
  },
  methods: {
    async getRequestedBooks() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          return alert('Access token is missing. Please log in again.');
        }

        const response = await fetch('http://127.0.0.1:5000/request', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        const data = await response.json();
        if (response.ok) {
          this.requestedBooks = data;
        } else {
          alert("Failed to fetch requested books");
        }
      } catch (error) {
        console.error('Error fetching requested books:', error);
      }
    },

    getRequestStatus(request) {
      if (request.is_approved) {
        return "Approved";
      } else if (request.is_rejected) {
        return "Rejected";
      } else if (request.is_returned) {
        return "Returned";
      } else if (request.is_requested) {
        return "Requested";
      } else {
        return "Unknown";
      }
    },

    async acceptRequest(requestId) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('Access token is missing. Please log in again.');
          return;
        }

        const response = await fetch(`http://127.0.0.1:5000/accept_request/${requestId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.getRequestedBooks();
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error('Error accepting request:', error);
      }
    },

    async rejectRequest(requestId) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('Access token is missing. Please log in again.');
          return;
        }

        const response = await fetch(`http://127.0.0.1:5000/reject_request/${requestId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.getRequestedBooks();
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error('Error rejecting request:', error);
      }
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
}

.table-container {
  display: flex;
  justify-content: center;
}

.requested-books-table {
  width: 80%; /* Adjust table width as needed */
  margin-top: 20px;
  border-collapse: collapse;
}

.requested-books-table th,
.requested-books-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.requested-books-table th {
  background-color: #f2f2f2;
}

.requested-books-table tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

.requested-books-table tbody tr:hover {
  background-color: #ddd;
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

.btn {
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
}

.btn-accept {
  background-color: green;
}

.btn-reject {
  background-color: red;
}

.btn:hover {
  opacity: 0.8;
}

.button-gap {
  margin-left: 10px;
}
</style>
