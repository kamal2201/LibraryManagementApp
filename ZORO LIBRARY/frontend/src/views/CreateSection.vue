<template>
    <div>
      <NavBar />
      <div class="background-image"></div>
      <div class="container">
        <h2>Add Section</h2>
        <form @submit.prevent="addSection" class="form">
          <div class="form-group">
            <label for="name">Name</label>
            <input v-model="name" type="text" id="name" required>
          </div>
          <div class="form-group">
            <label for="description">Description</label>
            <input v-model="description" type="text" id="description" required>
          </div>
          <button type="submit">Create</button>
        </form>
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
      name: '',
      description: ''
    };
  },
  methods: {
    async addSection() {
      try {
        const response = await fetch('http://127.0.0.1:5000/create_section', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            name: this.name,
            description: this.description
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push('/section');
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

input {
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
