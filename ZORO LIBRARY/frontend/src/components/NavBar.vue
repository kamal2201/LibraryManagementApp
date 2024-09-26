<template>
  <body>
    <nav class="navbar">
      <div class="container">
        <router-link class="navbar-brand" to="/">ZoroLibrary</router-link>
        <button class="navbar-toggler" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div :class="['navbar-collapse', { show: isNavbarOpen }]" id="navbarNavDropdown">
          <ul class="navbar-nav left">
            <li v-if="isloggedin" class="nav-item">
              <router-link class="nav-link" to="/section">Sections</router-link>
            </li>
            <li v-if="isloggedin" class="nav-item">
              <router-link class="nav-link" to="/book">Books</router-link>
            </li>
            <li v-if="isloggedin" class="nav-item">
              <router-link class="nav-link" to="/request">Requests</router-link>
            </li>
          </ul>
          <ul class="navbar-nav right">
            <li v-if="!isloggedin" class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li v-if="!isloggedin" class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
            <li v-if="isloggedin && this.email === 'librarian@gmail.com'" class="nav-item">
              <router-link class="nav-link" to="/admin_stats">Stats</router-link>
            </li>
            <li v-if="isloggedin && this.email === 'librarian@gmail.com'" class="nav-item">
              <router-link class="nav-link" to="/search">Search</router-link>
            </li>
            <li v-if="isloggedin && this.email !== 'librarian@gmail.com'" class="nav-item">
              <router-link class="nav-link" to="/my_books">My Books</router-link>
            </li>
            <li v-if="isloggedin && this.email !== 'librarian@gmail.com'" class="nav-item">
              <router-link class="nav-link" to="/search">Search</router-link>
            </li>
            <li v-if="isloggedin" class="nav-item">
              <a class="nav-link" @click="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </body>
</template>

<script>
import UserMixin from '../mixins/userMixin';

export default {
  mixins: [UserMixin],
  data() {
    return {
      isNavbarOpen: false,
      isDropdownOpen: false,
    };
  },
  methods: {
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
  },
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
}

.navbar {
  background-color: blue; /* Blue color */
  padding: 0.5rem; /* Reduce padding on the sides */
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  box-sizing: border-box;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 0 auto; /* Center the container */
  padding: 0; /* Remove padding on the sides */
  box-sizing: border-box;
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
  color: #ffffff;
  text-decoration: none; /* Remove underline */
  white-space: nowrap; /* Prevent wrapping */
}

.navbar-toggler {
  background: none;
  border: none;
  cursor: pointer;
}

.navbar-toggler-icon {
  width: 1.5rem;
  height: 1.5rem;
  background-color: #ffffff;
}

.navbar-collapse {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  flex-wrap: nowrap; /* Prevent wrapping */
  box-sizing: border-box;
}

.navbar-collapse.show {
  display: block;
}

.navbar-nav {
  list-style: none;
  padding-left: 0;
  display: flex;
  margin: 0;
  box-sizing: border-box;
}

.navbar-nav.left, .navbar-nav.right {
  display: flex;
  gap: 1rem; /* Add some space between items */
  box-sizing: border-box;
}

.nav-item {
  margin: 0;
}

.nav-link {
  text-decoration: none; /* Remove underline */
  color: #ffffff;
  cursor: pointer; /* Pointer cursor for links */
}

.nav-link:hover {
  text-decoration: none;
}

.dropdown-toggle::after {
  content: ' ▼';
}

.dropdown-menu {
  display: none;
  position: absolute;
  background-color: #007bff; /* Match navbar color */
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  padding: 0.5rem 0;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  padding: 0.25rem 1rem;
  text-decoration: none;
  color: #ffffff;
  display: block;
  cursor: pointer; /* Pointer cursor for dropdown items */
}

.dropdown-item:hover {
  background-color: #0056b3; /* Darker blue for hover */
  text-decoration: none; /* Remove underline on hover */
}

@media (
  max-width: 768px) {
  .navbar-collapse {
    flex-direction: column;
  }
  
  .navbar-nav {
    flex-direction: column;
  }
  
  .navbar-nav.left, .navbar-nav.right {
    margin: 0;
    gap: 0;
  }
  
  .navbar-nav.right {
    margin-top: 1rem;
  }
}
</style>

