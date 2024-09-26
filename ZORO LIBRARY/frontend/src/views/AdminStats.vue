<template>
  <div>
    <NavBar />
    <div class="background-image"></div>
    <div class="container">
      <h2><em>Admin Statistics</em></h2>
      <div class="stats-container">
        <div class="stat-card">
          <h3><em>User Stats</em></h3>
          <p>Total Users: {{ userStats.total_users }}</p>
          <p>Flagged Users: {{ userStats.flagged_users }}</p>
        </div>
        <div class="stat-card">
          <h3><em>Books and Sections</em></h3>
          <bar-chart :data="booksSectionStats"></bar-chart>
        </div>
        <div class="stat-card">
          <h3><em>Most Requested Book</em></h3>
          <p v-if="mostRequestedBook">
            Book Name: {{ mostRequestedBook.book_name }} <br />
            Author: {{ mostRequestedBook.author }} <br />
            Requests: {{ mostRequestedBook.request_count }}
          </p>
          <p v-else>
            No data available.
          </p>
        </div>
      </div>
      <a href="http://127.0.0.1:5000/download_csv" class="button">Download Report</a>
      
      <!-- Section for overdue users -->
      <div class="user-list overdue-users">
        <h3><em>Overdue Users</em></h3>
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in overdueUsers" :key="user.user_email">
              <td>{{ user.user_email }}</td>
              <td>{{ user.status || 'Overdue' }}</td>
              <td>
                <button 
                  v-if="user.status !== 'flagged'"
                  @click="flagUser(user.user_email)"
                >
                  Flag
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Section for flagged users -->
      <div class="user-list flagged-users">
        <h3><em>Flagged Users</em></h3>
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in flaggedUsers" :key="user.user_email">
              <td>{{ user.user_email }}</td>
              <td>Flagged</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import BarChart from './BarChart.vue';
import NavBar from '@/components/NavBar.vue';

export default {
  components: {
    BarChart,
    NavBar
  },
  data() {
    return {
      userStats: {
        total_users: 0,
        flagged_users: 0,
        overdue_users: [],
        all_users: []  // Include all users for complete list
      },
      booksSectionStats: [],
      mostRequestedBook: null,
      overdueUsers: [],
      flaggedUsers: []  // Separate list for flagged users
    };
  },
  mounted() {
    this.fetchAdminStats();
  },
  methods: {
    async fetchAdminStats() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          return alert('Access token is missing. Please log in again.');
        }

        const response = await fetch('http://127.0.0.1:5000/admin_stats', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.userStats = data.user_stats;
        this.booksSectionStats = data.books_section_stats;
        this.mostRequestedBook = data.most_requested_book;
        this.overdueUsers = data.user_stats.overdue_users.filter(user => user.status !== 'flagged');
        this.flaggedUsers = data.user_stats.all_users.filter(user => user.is_flagged);
      } catch (error) {
        console.error("Error fetching admin stats:", error);
      }
    },
    async flagUser(email) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          return alert('Access token is missing. Please log in again.');
        }

        const response = await fetch('http://127.0.0.1:5000/flag_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ email })
        });

        if (!response.ok) {
          if (response.status === 401) {
            alert('Unauthorized. Please log in again.');
          } else {
            throw new Error('Network response was not ok');
          }
        }

        const result = await response.json();
        alert(result.message || 'User flagged successfully!');

        // Update the lists
        this.fetchAdminStats();
      } catch (error) {
        console.error("Error flagging user:", error);
      }
    },
    async unflagUser(email) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          return alert('Access token is missing. Please log in again.');
        }

        const response = await fetch('http://127.0.0.1:5000/unflag_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ email })
        });

        if (!response.ok) {
          if (response.status === 401) {
            alert('Unauthorized. Please log in again.');
          } else {
            throw new Error('Network response was not ok');
          }
        }

        const result = await response.json();
        alert(result.message || 'User unflagged successfully!');
        
        this.fetchAdminStats();
      } catch (error) {
        console.error("Error unflagging user:", error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
  padding-top: 40px; /* Adjust this value as needed */
  max-width: 1200px;
  margin: 0 auto;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1;
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

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.stats-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 10px;
  flex: 1;
  min-width: 300px;
  max-width: 350px;
}

.stat-card h3 {
  margin-bottom: 20px;
  color: #666;
}

.stat-card p {
  margin: 10px 0;
  font-size: 16px;
  color: #444;
}

a.button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border-radius: 5px;
  text-align: center;
  text-decoration: none;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

a.button:hover {
  background-color: #0056b3;
}

.user-list {
  margin-top: 20px;
}

.user-list table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.user-list th, .user-list td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.user-list th {
  background-color: #f4f4f4;
  color: #333;
}

.user-list tr:nth-child(even) {
  background-color: #f9f9f9;
}

.user-list button {
  padding: 5px 10px;
  font-size: 14px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.user-list button:hover {
  background-color: #0056b3;
}
</style>
