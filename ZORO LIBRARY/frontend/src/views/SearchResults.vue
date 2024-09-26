<template>
  <NavBar />
  <div class="background-image"></div>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Search Results</h2>
    <div v-if="results.length">
      <div v-for="result in results" :key="result.id" class="result-item">
        <div v-if="result.description" class="section-result">
          <h4>Section: {{ result.name }}</h4>
          <p>{{ result.description }}</p>
          <button @click="viewSection(result.id)" class="btn btn-primary">Go to Section</button>
        </div>
        <div v-else class="book-result">
          <h4>Book: {{ result.name }}</h4>
          <p>Author: {{ result.author }} | Genre: {{ result.genre }}</p>
          <button @click="requestBook(result.id)" class="btn btn-success">Request Book</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No results found.</p>
    </div>
    <button @click="goBack" class="btn btn-secondary mt-4">Back to Search</button>
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
      results: []
    };
  },
  async created() {
    const query = this.$route.query.q;
    try {
      const response = await fetch(`http://127.0.0.1:5000/search?q=${query}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const data = await response.json();
      if (response.ok) {
        this.results = [...data.sections, ...data.books];
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.log(error);
    }
  },
  methods: {
    goBack() {
      this.$router.push({ name: 'search' });
    },
    async viewSection(id) {
      this.$router.push({ name: 'section', params: { id } });
    },
    async requestBook(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/request_book/${id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
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
  max-width: 800px; /* Adjusted for a wider container */
  margin: 30px auto; /* Added top and bottom margin */
  padding: 25px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-weight: 700;
}

.result-item {
  margin: 15px 0;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.section-result {
  background-color: #e0f7fa;
  padding: 15px;
  border-radius: 8px;
}

.book-result {
  background-color: #e8f5e9;
  padding: 15px;
  border-radius: 8px;
}

button {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
