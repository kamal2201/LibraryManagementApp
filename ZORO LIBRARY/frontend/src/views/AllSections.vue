<template>
    <NavBar />
    <div class="background-image"></div>
    <div class="container">
      <br>
      <h2><em>All Sections</em></h2>
      <div class="top-actions">
        <router-link v-if="isloggedin && this.email === 'librarian@gmail.com'" to="/create_section" class="btn btn-dark">Add Section</router-link>
      </div>
      <div class="sections-grid">
        <div v-for="section in sections" :key="section.id" class="section-card">
          <h3>{{ section.name }}</h3>
          <p>{{ section.description }}</p>
          <div class="button-group">
            <router-link v-if="isloggedin" :to="`/view_section/${section.id}`" class="btn btn-view">View</router-link>
            <router-link v-if="isloggedin && this.email === 'librarian@gmail.com'" :to="`/update_section/${section.id}`" class="btn btn-update">Update</router-link>
            <button v-if="isloggedin && this.email === 'librarian@gmail.com'" @click="deleteSection(section.id)" class="btn btn-delete">Delete</button>
          </div>
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
        sections: []
      }
    },
    created() {
      this.getSections();
    },
    methods: {
      async getSections() {
        try {
            const token = localStorage.getItem('access_token');
                if (!token) {
                    // Handle the case where the token is not available
                    return alert('Access token is missing. Please log in again.');
                }
                
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
            alert("Something went wrong");
          }
        } catch (error) {
          console.log(error);
        }
      },
  
      async deleteSection(id) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/delete_section/${id}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          });
          const data = await response.json();
          if (response.ok) {
            alert(data.message);
            this.getSections();
          } else {
            alert(data.error);
          }
        } catch (error) {
          console.log(error);
        }
      },
  
      viewSection(id) {
        console.log('Viewing section: ', id);
        // Add logic to navigate to the section view page or display a modal with details
      },

      async updateSection(sectionId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/update_section/${sectionId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({
              // Add data to update
            })
          });
          const data = await response.json();
          if (response.ok) {
            alert(data.message);
            this.getSections();
          } else {
            alert(data.error);
          }
        } catch (error) {
          console.log(error);
        }
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
  </style>
  