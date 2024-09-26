<template>
  <div>
    <NavBar/>
    <div class="background-image">
      <div class="page-content">
        <p><em>Discover worlds within words, explore realms in pages,</em></p>
        <p><em>Where stories unfold and imagination engages.</em></p>
        <p><em>In the library's embrace, knowledge takes flight,</em></p>
        <p><em>With each book a beacon, shining bright.</em></p>
        <p><em>Journey through literature's vast expanse, ignite your mind's delight.</em></p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'HomeView',
  components: {
    NavBar
  }
}
</script>

<style scoped>
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

  .page-content {
  position: absolute; /* Absolute positioning */
  top: 40%; /* Adjust the vertical position */
  left: 50%; /* Align content to the horizontal center */
  transform: translate(-50%, -50%); /* Center content */
  color: black; /* Text color */
  font-family: Arial, sans-serif; /* Font family */
  text-align: center; /* Center text */
  padding: 20px; /* Add padding for content */
  font-size: 125%; /* Increase font size by 25% */
}

.page-content p {
  margin-bottom: 10px; /* Add space between paragraphs */
  font-style: italic; /* Set text to italic */
}

/* Reset margin and padding for body and html elements */
body, html {
  margin: 0;
  padding: 0;
}

</style>
