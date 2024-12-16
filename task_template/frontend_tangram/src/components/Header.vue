<template>
  <div class="header-container">
    <div class="header-content">
      <h1>🤖🤝🧑 Collaborative AI Arena</h1>
      <h2 :style="{ fontWeight: 'normal' }">
        Benchmarking collaborative capabilities of AI in the wild
      </h2>
    </div>
    <nav class="navbar">
      <a href="https://leaderboard-draft.onrender.com/" target="_blank">Leaderboard</a>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Header"
}
</script>

<style scoped>
.header-container {
  background-color: rgb(76, 70, 163);
  color: white;
  display: flex;
  justify-content: space-between; 
  align-items: center; 
  height: 100%; 
  padding: 20px;
  max-height: 200px;
}

.navbar {
  color: white;
  display: flex;
}

.navbar a {
  padding: 5px;
}

a:link {
  color: white;
  background-color: transparent;
  text-decoration: none;
}

a:visited {
  color: white;
  background-color: transparent;
  text-decoration: none;
}

a:hover {
  color: red;
  background-color: transparent;
  text-decoration: underline;
}

a:active {
  color: yellow;
  background-color: transparent;
  text-decoration: underline;
}
</style>