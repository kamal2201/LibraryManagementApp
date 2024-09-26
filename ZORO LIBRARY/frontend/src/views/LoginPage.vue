<template>
    <div>
      <NavBar />
      <div class="background-image"></div>
      <div class="container">
        <h2>Login Here</h2>
        <form @submit.prevent="login" class="form">
          <div class="form-group">
            <label for="email">Email address</label>
            <input v-model="email" type="email" id="email" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input v-model="password" type="password" id="password" required>
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import NavBar from '@/components/NavBar.vue';
  
  export default {
    data() {
      return {
        email: '',
        password: ''
      }
    },
    methods: {
      async login() {
        try {
          const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password
            })
          });
          const data = await response.json();
          if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            alert(data.message);
            this.$router.push('/');
          } else {
            console.log(data.error);
            alert(data.error);
          }
        } catch (error) {
          console.log(error);
          alert(error);
        }
      }
    },
    components: {
      NavBar
    }
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
  
  body {
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
  }
  
  .background-image {
    /* Set background image */
    background-image: url('../assets/background.jpg'); /* Change path to your image */
    /* Adjust background properties */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    /* Set dimensions to cover entire viewport */
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -1; /* Ensure it's behind other elements */
  }
  
  .container {
    width: 100%;
    max-width: 500px;
    margin: auto;
    padding: 25px;
    background: rgba(255, 255, 255, 0.7); /* Adjust opacity as needed */
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
  
  .form-text {
    font-size: 12px;
    color: #666;
    margin-top: 5px;
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
  